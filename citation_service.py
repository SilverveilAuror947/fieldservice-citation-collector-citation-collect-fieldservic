"""Compatibility import for running the project directly from a checkout."""

from src.citation_service import (  # noqa: F401
    InfraiClient,
    InfraiError,
    ResearchNote,
    collect_citations,
    openai_embedder,
)

__all__ = [
    "InfraiClient",
    "InfraiError",
    "ResearchNote",
    "collect_citations",
    "openai_embedder",
]
