
def _writeGuidelines(
    glyphObject: Any, element: ElementType, identifiers: set[str], validate: bool
) -> None:
    guidelines = getattr(glyphObject, "guidelines", [])
    if validate and not guidelinesValidator(guidelines):
        raise GlifLibError("guidelines attribute does not have the proper structure.")
    for guideline in guidelines:
        attrs = OrderedDict()
        x = guideline.get("x")
        if x is not None:
            attrs["x"] = repr(x)
        y = guideline.get("y")
        if y is not None:
            attrs["y"] = repr(y)
        angle = guideline.get("angle")
        if angle is not None:
            attrs["angle"] = repr(angle)
        name = guideline.get("name")
        if name is not None:
            attrs["name"] = name
        color = guideline.get("color")
        if color is not None:
            attrs["color"] = color
        identifier = guideline.get("identifier")
        if identifier is not None:
            if validate and identifier in identifiers:
                raise GlifLibError("identifier used more than once: %s" % identifier)
            attrs["identifier"] = identifier
            identifiers.add(identifier)
        etree.SubElement(element, "guideline", attrs)

