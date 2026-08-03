from typing import Any, Dict, Optional, Union

def _get_wrapper_timeout(
    kwargs: Dict[str, Any], exception: Exception
) -> Optional[Union[float, int, httpx.Timeout]]:
    """
    Get the timeout from the kwargs
    Used for the wrapper functions.
    """

    timeout = cast(
        Optional[Union[float, int, httpx.Timeout]], kwargs.get("timeout", None)
    )

    return timeout

