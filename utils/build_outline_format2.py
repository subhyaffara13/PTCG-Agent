
def buildOutlineFormat2(
    glyphObject: Any,
    pen: AbstractPointPen,
    outline: Iterable[ElementType],
    identifiers: set[str],
    validate: bool,
) -> None:
    for element in outline:
        if element.tag == "contour":
            _buildOutlineContourFormat2(pen, element, identifiers, validate)
        elif element.tag == "component":
            _buildOutlineComponentFormat2(pen, element, identifiers, validate)
        else:
            raise GlifLibError("Unknown element in outline element: %s" % element.tag)

