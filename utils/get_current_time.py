from typing import Any, Dict, Optional

def get_current_time(params: Optional[Dict[str, Any]] = None) -> str:
    """
    Get the current time (hardcoded sample implementation)

    Args:
        params: Optional dictionary with parameters
            - format: The format of the time to return (e.g., "short")

    Returns:
        A string representing the current time
    """
    # Hardcoded time value for sample implementation
    if params and params.get("format") == "short":
        return "10:30 AM"
    return "10:30:45 AM"

