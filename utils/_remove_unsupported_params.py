from typing import List, Optional

def _remove_unsupported_params(
    non_default_params: dict, supported_openai_params: Optional[List[str]]
) -> dict:
    """
    Remove unsupported params from non_default_params
    """
    remove_keys = []
    if supported_openai_params is None:
        return {}  # no supported params, so no optional openai params to send
    for param in non_default_params.keys():
        if param not in supported_openai_params:
            remove_keys.append(param)
    for key in remove_keys:
        non_default_params.pop(key, None)
    return non_default_params

