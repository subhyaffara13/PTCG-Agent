from typing import Any

def _writeAnchorsFormat1(pen: Any, anchors: Any, validate: bool) -> None:
    if validate and not anchorsValidator(anchors):
        raise GlifLibError("anchors attribute does not have the proper structure.")
    for anchor in anchors:
        attrs = {}
        x = anchor["x"]
        attrs["x"] = repr(x)
        y = anchor["y"]
        attrs["y"] = repr(y)
        name = anchor.get("name")
        if name is not None:
            attrs["name"] = name
        pen.beginPath()
        pen.addPoint((x, y), segmentType="move", name=name)
        pen.endPath()

