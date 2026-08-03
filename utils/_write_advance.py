from typing import Any

def _writeAdvance(glyphObject: Any, element: ElementType, validate: bool) -> None:
    width = getattr(glyphObject, "width", None)
    if width is not None:
        if validate and not isinstance(width, numberTypes):
            raise GlifLibError("width attribute must be int or float")
        if width == 0:
            width = None
    height = getattr(glyphObject, "height", None)
    if height is not None:
        if validate and not isinstance(height, numberTypes):
            raise GlifLibError("height attribute must be int or float")
        if height == 0:
            height = None
    if width is not None and height is not None:
        etree.SubElement(
            element,
            "advance",
            OrderedDict([("height", repr(height)), ("width", repr(width))]),
        )
    elif width is not None:
        etree.SubElement(element, "advance", dict(width=repr(width)))
    elif height is not None:
        etree.SubElement(element, "advance", dict(height=repr(height)))

