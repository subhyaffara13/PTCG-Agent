from typing import Any

def _key_was_scim_blocked(metadata: Any) -> bool:
    """True if a verification token carries the SCIM-block marker in metadata."""
    return (
        isinstance(metadata, dict) and metadata.get(SCIM_BLOCKED_METADATA_KEY) is True
    )

