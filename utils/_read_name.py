from typing import Any, Optional

def _readName(glyphObject: Optional[Any], root: ElementType, validate: bool) -> None:
    glyphName = root.get("name")
    if validate and not glyphName:
        raise GlifLibError("Empty glyph name in GLIF.")
    if glyphName and glyphObject is not None:
        _relaxedSetattr(glyphObject, "name", glyphName)

