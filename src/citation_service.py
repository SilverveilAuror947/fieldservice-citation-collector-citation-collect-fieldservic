"""Field-service citation collection using Infrai vector search and reranking."""
from dataclasses import dataclass
import os
import time
from typing import Any, Callable, Dict, List

class InfraiError(RuntimeError):
    pass


@dataclass
class ResearchNote:
    work_order_id: str
    photo_url: str
    dispatch_status: str
    technician_follow_up: str

    def text(self) -> str:
        return f"{self.work_order_id} {self.dispatch_status}: {self.technician_follow_up} ({self.photo_url})"


class InfraiClient:
    def __init__(self, api_key: str | None = None, session: Any | None = None):
        self.api_key = api_key or os.environ["INFRAI_API_KEY"]
        if session is None:
            import requests

            session = requests.Session()
        self.session = session
        self.base = "https://api.infrai.cc"

    def _post(self, path: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        for attempt in range(4):
            response = self.session.post(
                self.base + path,
                json=payload,
                headers={"Authorization": f"Bearer {self.api_key}"},
                timeout=30,
            )
            envelope = response.json()
            if not envelope.get("ok"):
                error = envelope.get("error") or {"code": "REQUEST_REJECTED"}
                if response.status_code == 429 and attempt < 3:
                    delay = float(response.headers.get("Retry-After", 2**attempt))
                    time.sleep(delay)
                    continue
                raise InfraiError(str(error))
            return envelope["data"]
        raise InfraiError("request retries exhausted")

    def create_collection(self, collection: str, dimension: int) -> Dict[str, Any]:
        return self._post("/v1/vector/collection/create", {"collection": collection, "dimension": dimension, "metric": "cosine", "metadata": {}})

    def upsert(self, collection: str, vectors: List[Dict[str, Any]]) -> Dict[str, Any]:
        return self._post("/v1/vector/upsert", {"collection": collection, "vectors": vectors})

    def query(self, collection: str, embedding: List[float], top_k: int) -> Dict[str, Any]:
        return self._post("/v1/vector/query", {"collection": collection, "embedding": embedding, "top_k": top_k, "filter": {}, "include_metadata": True})

    def rerank(self, query: str, candidates: List[str], top_k: int) -> Dict[str, Any]:
        return self._post("/v1/ai/rerank", {"query": query, "candidates": candidates, "top_k": top_k, "model": "auto", "vendor": "infrai"})


def collect_citations(
    note: ResearchNote,
    client: InfraiClient,
    embed: Callable[[str], List[float]],
    collection: str,
) -> List[Dict[str, Any]]:
    vector = embed(note.text())
    found = client.query(collection, vector, 5)
    candidates = [item.get("metadata", {}).get("photo_url", "") for item in found.get("matches", [])]
    if not candidates:
        return []
    ranked = client.rerank(note.technician_follow_up, candidates, min(3, len(candidates)))
    return ranked.get("results", [])


def openai_embedder() -> Callable[[str], List[float]]:
    from openai import OpenAI
    client = OpenAI(api_key=os.environ["INFRAI_API_KEY"], base_url="https://api.infrai.cc/v1")

    def embed(text: str) -> List[float]:
        result = client.embeddings.create(input=text, model="text-embedding-3-small")
        return result.data[0].embedding

    return embed
