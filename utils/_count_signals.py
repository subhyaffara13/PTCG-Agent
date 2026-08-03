import re
from typing import List

def _count_signals(text: str, patterns: List[str]) -> int:
    """Count how many of the patterns appear in text."""
    return sum(1 for p in patterns if re.search(p, text, re.IGNORECASE))

