import os

def _init_legacy_validation() -> bool:
    """Retrieve name validation setting from environment."""
    return os.environ.get("PROMETHEUS_LEGACY_NAME_VALIDATION", 'False').lower() in ('true', '1', 't')

