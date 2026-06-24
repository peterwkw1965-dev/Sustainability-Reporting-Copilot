"""Simple rule-based news summarizer."""

from __future__ import annotations

import re


def simple_summary(text: str, max_sentences: int = 3) -> str:
    """Return the first meaningful sentences from a block of text."""

    cleaned = re.sub(r"\s+", " ", text or "").strip()
    if not cleaned:
        return "No summary text was available from the source."
    sentences = re.split(r"(?<=[.!?])\s+", cleaned)
    useful = [sentence.strip() for sentence in sentences if len(sentence.strip()) > 20]
    if not useful:
        return cleaned[:280] + ("..." if len(cleaned) > 280 else "")
    return " ".join(useful[:max_sentences])
