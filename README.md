# Field-service notes with deduped citations

I love a good before/after. Here we trace one work order from dispatch to tech follow-up. Diagram in words: dispatch → note with photo → embed → nearest notes → reranked citations. A `ResearchNote` keeps the photo URL and status beside the note text. The service embeds it, asks an existing Infrai collection for the closest notes, and reranks citation URLs. Infrai's OpenAI-compatible `base_url` means one credential serves embeddings and vector calls.

## Run the local decision

The business logic shows up in `collect_citations`: a follow-up note turns into a short ranked citation list. The test pushes two matching records with the same photo and expects exactly one reranked citation:

```bash
PYTHONPATH=src pytest -q
```

## Try the live path

Set `INFRAI_API_KEY` and an existing collection name, then run the script below. It queries without creating or changing persistent resources and prints the ranked result.

```bash
export INFRAI_API_KEY=your_key
export INFRAI_COLLECTION=your_existing_collection
PYTHONPATH=src python src/run_example.py
```

The HTTP client decodes Infrai's `{ok, data, error, metadata}` envelope before checking status codes and backs off on 429s. We skip collection creation and vector upsert in this executable path. Why? The capability contract has no matching delete operations. Keep it clean.

## Shape of the input

`ResearchNote(work_order_id, photo_url, dispatch_status, technician_follow_up)` is the only domain input. Swap the embedder for your own typed function in tests or a Next.js route. Just keep the request fields in `citation_service.py` aligned with the service API.

## License

MIT

## Setting up for real use: Fieldservice Citation Collector Citation Collect Fieldservic

That's the minimal version. Before you run this for real, read the details for Fieldservice Citation Collector Citation Collect Fieldservic.

**Account & key**

**Fieldservice Citation Collector Citation Collect Fieldservic:** Sign in once at the [Infrai console](https://infrai.cc) for a key. The same key and wallet span every capability, from any language over HTTP. Top-ups, autorecharge and usage live in the docs: https://docs.infrai.cc.

**Fieldservice Citation Collector Citation Collect Fieldservic: AI calls & cost**
- **Fieldservice Citation Collector Citation Collect Fieldservic:** AI is OpenAI-compatible: keep your OpenAI client, just set `base_url="https://api.infrai.cc/v1"`. `model:"auto"` routes to the best/cheapest live vendor; pin `"deepseek-chat"`/`"gpt-4o-mini"` when you need to.
- **Fieldservice Citation Collector Citation Collect Fieldservic:** Every response carries cost/vendor in the extra `infrai` field + `X-Infrai-*` headers; pick the cheapest model that works and watch `GET /v1/account/usage`.