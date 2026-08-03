from typing import Any, Optional

def _buildAnchorFormat1(point: ElementType, validate: bool) -> Optional[dict[str, Any]]:
    if point.get("type") != "move":
        return None
    name = point.get("name")
    if name is None:
        return None
    x = point.get("x")
    y = point.get("y")
    if validate and x is None:
        raise GlifLibError("Required x attribute is missing in point element.")
    assert x is not None
    if validate and y is None:
        raise GlifLibError("Required y attribute is missing in point element.")
    assert y is not None
    x = _number(x)
    y = _number(y)
    anchor = dict(x=x, y=y, name=name)
    return anchor

