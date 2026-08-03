from typing import Any, Dict, Optional

def _redact_settings(settings: Optional[Mapping[str, Any]]) -> Dict[str, Any]:
    """Replace every value in a settings map with a fixed marker.

    Cache config carries Redis credentials (passwords, connection strings).
    The audit-log row preserves the field names so a reader can see *which*
    fields changed, but values are stripped so the audit table can't itself
    become a credential-harvest sink.
    """
    if not settings:
        return {}
    return {k: _REDACTED_VALUE for k in settings.keys()}

