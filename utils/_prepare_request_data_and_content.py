from typing import Any, Optional, Tuple, Union

def _prepare_request_data_and_content(
    data: Optional[Union[dict, str, bytes]] = None,
    content: Any = None,
) -> Tuple[Optional[Union[dict, Mapping]], Any]:
    """
    Helper function to route data/content parameters correctly for httpx requests

    This prevents httpx DeprecationWarnings that cause memory leaks.

    Background:
    - httpx shows a DeprecationWarning when you pass bytes/str to `data=`
    - It wants you to use `content=` instead for bytes/str
    - The warning itself leaks memory when triggered repeatedly

    Solution:
    - Move bytes/str from `data=` to `content=` before calling build_request
    - Keep dicts in `data=` (that's still the correct parameter for dicts)

    Args:
        data: Request data (can be dict, str, or bytes)
        content: Request content (raw bytes/str)

    Returns:
        Tuple of (request_data, request_content) properly routed for httpx
    """
    request_data = None
    request_content = content

    if data is not None:
        if isinstance(data, (bytes, str)):
            # Bytes/strings belong in content= (only if not already provided)
            if content is None:
                request_content = data
        else:
            # dict/Mapping stays in data= parameter
            request_data = data

    return request_data, request_content

