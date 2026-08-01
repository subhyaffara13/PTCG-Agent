
def _readAdvance(glyphObject: Optional[Any], advance: ElementType) -> None:
    width = _number(advance.get("width", 0))
    _relaxedSetattr(glyphObject, "width", width)
    height = _number(advance.get("height", 0))
    _relaxedSetattr(glyphObject, "height", height)

