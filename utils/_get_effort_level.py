from typing import Optional, Union

def _get_effort_level(value: Union[str, dict, None]) -> Optional[str]:
    """Extract the effective effort level from reasoning_effort (string or dict).

    Use this for guards that compare effort level (e.g. xhigh validation, "none" checks).
    Ensures dict inputs like {"effort": "none", "summary": "detailed"} are correctly
    treated as effort="none" for validation purposes.
    """
    if value is None:
        return None
    if isinstance(value, str):
        return value
    if isinstance(value, dict) and "effort" in value:
        return value["effort"]
    return None

