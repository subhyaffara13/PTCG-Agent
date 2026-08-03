from typing import Optional

def _extract_summary_text(raw: Optional[str]) -> Optional[str]:
    if not raw:
        return None
    match = _SUMMARY_TAG_RE.search(raw)
    if match is None:
        return None
    summary = match.group(1).strip()
    return summary or None

