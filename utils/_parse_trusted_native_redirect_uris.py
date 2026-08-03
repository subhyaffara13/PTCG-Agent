import os
from typing import List

def _parse_trusted_native_redirect_uris() -> List[str]:
    """Built-in native MCP callbacks plus ``MCP_TRUSTED_NATIVE_REDIRECT_URIS``."""
    entries: List[str] = [uri.lower() for uri in _DEFAULT_NATIVE_REDIRECT_URIS]
    raw = os.environ.get(_TRUSTED_NATIVE_REDIRECT_URIS_ENV, "").strip()
    if not raw:
        return entries
    for token in raw.split(","):
        entry = token.strip().lower()
        if entry and entry not in entries:
            entries.append(entry)
    return entries

