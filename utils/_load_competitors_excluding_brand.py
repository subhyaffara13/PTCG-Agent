import json
from typing import List, Set

def _load_competitors_excluding_brand(brand_self: List[str]) -> List[str]:
    """
    Load competitor tokens from major_airlines.json (harm_toxic_abuse-style format).
    Exclude any airline whose id or match variants overlap with brand_self.
    Returns a flat list of match variants (pipe-separated values) from non-excluded airlines.
    """
    brand_set = {b.lower().strip() for b in brand_self if b}
    if not _MAJOR_AIRLINES_PATH.exists():
        return []
    try:
        with open(_MAJOR_AIRLINES_PATH, encoding="utf-8") as f:
            airlines = json.load(f)
    except (json.JSONDecodeError, OSError):
        return []
    result: List[str] = []
    for entry in airlines:
        if not isinstance(entry, dict):
            continue
        match_str = entry.get("match") or ""
        variants = [v.strip().lower() for v in match_str.split("|") if v.strip()]
        words_in_match: Set[str] = set()
        for v in variants:
            words_in_match.update(v.split())
        if brand_set & words_in_match or any(v in brand_set for v in variants):
            continue
        result.extend(variants)
    return result

