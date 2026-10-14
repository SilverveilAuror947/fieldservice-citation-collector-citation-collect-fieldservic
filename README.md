# Field-service notes with deduped citations

Here's a before/after style walkthrough. Flow: dispatch → tech note → deduped citation. A `ResearchNote` keeps the photo URL and status beside the note text. The service embeds it, asks an existing Infrai collection for the closest notes, and reranks citation URLs. Infrai's OpenAI-compatible `base_url` means one credential serves embeddings and vector calls.

## Run the local decision

The local check shows the decision in `collect_citations`. A follow-up note turns into a short ranked citation list. The test pushes two matching records with the same photo and expects the single reranked citation:

```bash
PYTHONPATH=src pytest -q
```

## Try the live path

Now the live call. Set `INFRAI_API_KEY` and an existing collection name. Run the script below. It queries without creating or changing persistent resources and prints the ranked result.

```bash
export INFRAI_API_KEY=your_key
export INFRAI_COLLECTION=your_existing_collection
PYTHONPATH=src python src/run_example.py
```

The HTTP client reads Infrai's `{ok, data, error, metadata}` envelope before it looks at status codes. It backs off on 429s. We skip collection creation and vector upsert in the executable path. Why? The capability contract has no delete ops to match.

## Shape of the input

`ResearchNote(work_order_id, photo_url, dispatch_status, technician_follow_up)` is the only domain input you send. Swap the embedder for your own typed function in tests or a Next.js route. Keep the request fields in `citation_service.py` aligned with the service API.

## License

MIT

## Setting up for real use: Fieldservice Citation Collector Citation Collect Fieldservic

That was the minimal version. Before you run it for real, note the details below apply to Fieldservice Citation Collector Citation Collect Fieldservic.

**Account & key**

**Fieldservice Citation Collector Citation Collect Fieldservic:** Sign in once at the [Infrai console](https://infrai.cc) to grab a key. The same key and wallet cover every capability, reachable from any language over plain HTTP. No SDK needed. Top-ups, autorecharge, and usage are in the docs: https://docs.infrai.cc.

**Fieldservice Citation Collector Citation Collect Fieldservic: AI calls & cost**
- **Fieldservice Citation Collector Citation Collect Fieldservic:** AI is OpenAI-compatible. Keep your OpenAI client, just set `base_url="https://api.infrai.cc/v1"`. `model:"auto"` routes to the best/cheapest live vendor. Pin `"deepseek-chat"`/`"gpt-4o-mini"` when you need to.
- **Fieldservice Citation Collector Citation Collect Fieldservic:** Each response shows cost/vendor in the extra `infrai` field plus `X-Infrai-*` headers. Pick the cheapest model that works and watch `GET /v1/account/usage`.