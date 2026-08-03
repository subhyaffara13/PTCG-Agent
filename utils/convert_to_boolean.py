from typing import Any

def convert_to_boolean(value: Any | None) -> bool:
    """Return a boolean value translating from other types if necessary."""
    if isinstance(value, bool):
        return value
    if not isinstance(value, str):
        value = str(value)
    if value.lower() not in configparser.RawConfigParser.BOOLEAN_STATES:
        raise ValueError(f"Not a boolean: {value}")
    return configparser.RawConfigParser.BOOLEAN_STATES[value.lower()]

