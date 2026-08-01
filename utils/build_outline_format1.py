
def buildOutlineFormat1(
    glyphObject: Any,
    pen: Optional[AbstractPointPen],
    outline: Iterable[ElementType],
    validate: bool,
) -> None:
    anchors = []
    for element in outline:
        if element.tag == "contour":
            if len(element) == 1:
                point = element[0]
                if point.tag == "point":
                    anchor = _buildAnchorFormat1(point, validate)
                    if anchor is not None:
                        anchors.append(anchor)
                        continue
            if pen is not None:
                _buildOutlineContourFormat1(pen, element, validate)
        elif element.tag == "component":
            if pen is not None:
                _buildOutlineComponentFormat1(pen, element, validate)
        else:
            raise GlifLibError("Unknown element in outline element: %s" % element)
    if glyphObject is not None and anchors:
        if validate and not anchorsValidator(anchors):
            raise GlifLibError("GLIF 1 anchors are not properly formatted.")
        _relaxedSetattr(glyphObject, "anchors", anchors)

