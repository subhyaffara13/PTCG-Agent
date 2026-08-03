from typing import Optional, Set

def _tokens(text: Optional[str]) -> Set[str]:
    if not text:
        return set()
    return {t.lower() for t in _TOKEN_RE.findall(text)}

