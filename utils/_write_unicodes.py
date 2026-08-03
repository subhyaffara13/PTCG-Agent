from typing import Any

def _writeUnicodes(glyphObject: Any, element: ElementType, validate: bool) -> None:
    unicodes = getattr(glyphObject, "unicodes", [])
    if validate and isinstance(unicodes, int):
        unicodes = [unicodes]
    seen = set()
    for code in unicodes:
        if validate and not isinstance(code, int):
            raise GlifLibError("unicode values must be int")
        if code in seen:
            continue
        seen.add(code)
        hexCode = "%04X" % code
        etree.SubElement(element, "unicode", dict(hex=hexCode))

