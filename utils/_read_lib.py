from typing import Any, Optional

def _readLib(glyphObject: Optional[Any], lib: ElementType, validate: bool) -> None:
    assert len(lib) == 1
    child = lib[0]
    plist = plistlib.fromtree(child)
    if validate:
        valid, message = glyphLibValidator(plist)
        if not valid:
            raise GlifLibError(message)
    _relaxedSetattr(glyphObject, "lib", plist)

