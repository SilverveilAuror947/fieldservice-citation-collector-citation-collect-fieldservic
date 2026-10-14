from citation_service import ResearchNote, collect_citations


class FakeClient:
    def __init__(self):
        self.queried_collection = None

    def query(self, collection, embedding, top_k):
        self.queried_collection = collection
        return {"matches": [{"metadata": {"photo_url": "https://example.com/a.jpg"}}, {"metadata": {"photo_url": "https://example.com/a.jpg"}}]}
    def rerank(self, query, candidates, top_k):
        return {"results": [{"document": candidates[0], "score": 0.9}]}


def test_collects_one_ranked_citation_for_follow_up():
    note = ResearchNote("WO-1", "https://example.com/photo.jpg", "en_route", "Sensor replaced")
    client = FakeClient()
    result = collect_citations(note, client, lambda text: [0.1, 0.2], "existing-notes")
    assert result == [{"document": "https://example.com/a.jpg", "score": 0.9}]
    assert client.queried_collection == "existing-notes"
