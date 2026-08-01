
def _writeLib(glyphObject: Any, element: ElementType, validate: bool) -> None:
    lib = getattr(glyphObject, "lib", None)
    if not lib:
        # don't write empty lib
        return
    if validate:
        valid, message = glyphLibValidator(lib)
        if not valid:
            raise GlifLibError(message)
    if not isinstance(lib, dict):
        lib = dict(lib)
    # plist inside GLIF begins with 2 levels of indentation
    e = plistlib.totree(lib, indent_level=2)
    etree.SubElement(element, "lib").append(e)

