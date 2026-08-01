
def is_jsonable(obj: Any, _visited: set[int] | None = None) -> bool:
    """Check if an object is JSON serializable.

    This is a weak check, as it does not check for the actual JSON serialization, but only for the types of the object.
    It works correctly for basic use cases but do not guarantee an exhaustive check.

    Object is considered to be recursively json serializable if:
    - it is an instance of int, float, str, bool, or NoneType
    - it is a list or tuple and all its items are json serializable
    - it is a dict and all its keys are strings and all its values are json serializable

    Uses a visited set to avoid infinite recursion on circular references. If object has already been visited, it is
    considered not json serializable.
    """
    # Initialize visited set to track object ids and detect circular references
    if _visited is None:
        _visited = set()

    # Detect circular reference
    obj_id = id(obj)
    if obj_id in _visited:
        return False

    # Add current object to visited before recursive checks
    _visited.add(obj_id)
    try:
        if isinstance(obj, _JSON_SERIALIZABLE_TYPES):
            return True
        if isinstance(obj, (list, tuple)):
            return all(is_jsonable(item, _visited) for item in obj)
        if isinstance(obj, dict):
            return all(
                isinstance(key, _JSON_SERIALIZABLE_TYPES) and is_jsonable(value, _visited)
                for key, value in obj.items()
            )
        if hasattr(obj, "__json__"):
            return True
        return False
    except RecursionError:
        return False
    finally:
        # Remove the object id from visited to avoid side‑effects for other branches
        _visited.discard(obj_id)

