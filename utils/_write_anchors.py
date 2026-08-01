
def _writeAnchors(
    glyphObject: Any,
    element: ElementType,
    identifiers: set[str],
    validate: bool,
) -> None:
    anchors = getattr(glyphObject, "anchors", [])
    if validate and not anchorsValidator(anchors):
        raise GlifLibError("anchors attribute does not have the proper structure.")
    for anchor in anchors:
        attrs = OrderedDict()
        x = anchor["x"]
        attrs["x"] = repr(x)
        y = anchor["y"]
        attrs["y"] = repr(y)
        name = anchor.get("name")
        if name is not None:
            attrs["name"] = name
        color = anchor.get("color")
        if color is not None:
            attrs["color"] = color
        identifier = anchor.get("identifier")
        if identifier is not None:
            if validate and identifier in identifiers:
                raise GlifLibError("identifier used more than once: %s" % identifier)
            attrs["identifier"] = identifier
            identifiers.add(identifier)
        etree.SubElement(element, "anchor", attrs)

