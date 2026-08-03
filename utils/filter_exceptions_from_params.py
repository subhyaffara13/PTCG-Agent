from typing import Any

def filter_exceptions_from_params(data: Any, max_depth: int = 20) -> Any:
    """
    Recursively filter out Exception objects and callable objects from dicts/lists.

    This is a defensive utility to prevent deepcopy failures when exception objects
    are accidentally stored in parameter dictionaries (e.g., optional_params).
    Also filters callable objects (functions) to prevent JSON serialization errors.
    Exceptions and callables should not be stored in params - this function removes them.

    Args:
        data: The data structure to filter (dict, list, or any other type)
        max_depth: Maximum recursion depth to prevent infinite loops

    Returns:
        Filtered data structure with Exception and callable objects removed, or None if the
        entire input was an Exception or callable
    """
    if max_depth <= 0:
        return data

    # Skip exception objects
    if isinstance(data, Exception):
        return None
    # Skip callable objects (functions, methods, lambdas) but not classes (type objects)
    if callable(data) and not isinstance(data, type):
        return None
    # Skip known non-serializable object types (Logging, Router, etc.)
    obj_type_name = type(data).__name__
    if obj_type_name in ["Logging", "LiteLLMLoggingObj", "Router"]:
        return None

    if isinstance(data, dict):
        result: dict[str, Any] = {}
        for k, v in data.items():
            # Skip exception and callable values
            if isinstance(v, Exception) or (callable(v) and not isinstance(v, type)):
                continue
            try:
                filtered = filter_exceptions_from_params(v, max_depth - 1)
                if filtered is not None:
                    result[k] = filtered
            except Exception:
                # Skip values that cause errors during filtering
                continue
        return result
    elif isinstance(data, list):
        result_list: list[Any] = []
        for item in data:
            # Skip exception and callable items
            if isinstance(item, Exception) or (
                callable(item) and not isinstance(item, type)
            ):
                continue
            try:
                filtered = filter_exceptions_from_params(item, max_depth - 1)
                if filtered is not None:
                    result_list.append(filtered)
            except Exception:
                # Skip items that cause errors during filtering
                continue
        return result_list
    else:
        return data

