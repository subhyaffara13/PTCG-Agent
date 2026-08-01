
def is_supported_id(value: str) -> bool:
    """Validate SPDX-ID according to current spec."""
    return value in __IDS

