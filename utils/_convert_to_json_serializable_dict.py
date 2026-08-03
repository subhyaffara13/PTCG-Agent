from typing import Any, Optional

def _convert_to_json_serializable_dict(
    obj: Any, visited: Optional[set] = None, max_depth: int = 20
) -> Any:
    """
    Convert object to JSON-serializable dict, handling Pydantic models safely.

    This avoids pickle-based deepcopy which fails on Pydantic v2 models
    containing _thread.RLock objects.

    Args:
        obj: Object to convert (dict, list, Pydantic model, or primitive)
        visited: Set of object IDs to track circular references
        max_depth: Maximum recursion depth to prevent infinite recursion

    Returns:
        JSON-serializable version of the object
    """
    if max_depth <= 0:
        # Return a placeholder if max depth is exceeded
        return "<max_depth_exceeded>"

    if visited is None:
        visited = set()

    # Get the object's memory address to track visited objects
    obj_id = id(obj)
    if obj_id in visited:
        # Circular reference detected, return placeholder
        return "<circular_reference>"

    # Only track mutable objects (dict, list, objects with __dict__)
    if isinstance(obj, (dict, list)) or hasattr(obj, "__dict__"):
        visited.add(obj_id)

    try:
        if isinstance(obj, BaseModel):
            # Use Pydantic's model_dump() instead of pickle
            result = obj.model_dump()
            # Recursively process the dumped dict
            return _convert_to_json_serializable_dict(result, visited, max_depth - 1)
        elif isinstance(obj, dict):
            return {
                k: _convert_to_json_serializable_dict(v, visited, max_depth - 1)
                for k, v in obj.items()
            }
        elif isinstance(obj, list):
            return [
                _convert_to_json_serializable_dict(item, visited, max_depth - 1)
                for item in obj
            ]
        elif hasattr(obj, "__dict__"):
            # Handle objects with __dict__ attribute
            return _convert_to_json_serializable_dict(
                obj.__dict__, visited, max_depth - 1
            )
        else:
            # Primitives (str, int, float, bool, None) pass through
            return obj
    finally:
        # Remove from visited set when done processing this object
        if obj_id in visited:
            visited.remove(obj_id)

