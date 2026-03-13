"""Shared utility functions used across pipeline steps."""

import re
import pandas as pd


def is_trivial_response(response_text: object) -> bool:
    """Return True if the response carries no meaningful content."""
    if pd.isna(response_text):
        return True

    text = str(response_text).strip().lower()
    text_clean = re.sub(r'[^\w\s]', '', text)

    trivial = {
        'no', 'nope', 'na', 'n/a', 'nothing', 'none', 'not really',
        'nah', 'nada', 'idk', 'dont know', 'not sure', 'no idea', '',
    }

    return text_clean in trivial or len(text_clean) <= 2


def parse_llm_category_lines(llm_output: str, max_categories: int = 3) -> list[str]:
    """
    Parse newline-separated category names from raw LLM output.

    Strips leading bullet/number prefixes; ignores blank or overlong lines.
    Returns at most *max_categories* entries (or ["Other"] if none found).
    """
    categories = []
    for line in llm_output.split('\n'):
        line = line.strip()
        line = line.lstrip('•-*123456789. ')
        if line and 2 < len(line) < 60:
            categories.append(line)
        if len(categories) == max_categories:
            break
    return categories if categories else ["Other"]
