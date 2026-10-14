import json
import os

from citation_service import ResearchNote, InfraiClient, collect_citations, openai_embedder


if __name__ == "__main__":
    note = ResearchNote("WO-1042", "https://example.com/pump.jpg", "dispatched", "Replaced the pressure sensor; verify readings tomorrow.")
    collection = os.environ["INFRAI_COLLECTION"]
    citations = collect_citations(note, InfraiClient(), openai_embedder(), collection)
    print(json.dumps({"work_order": note.work_order_id, "citations": citations}, indent=2))
