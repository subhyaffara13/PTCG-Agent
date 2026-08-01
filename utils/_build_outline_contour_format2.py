
def _buildOutlineContourFormat2(
    pen: AbstractPointPen, contour: ElementType, identifiers: set[str], validate: bool
) -> None:
    if validate:
        for attr in contour.attrib.keys():
            if attr not in contourAttributesFormat2:
                raise GlifLibError("Unknown attribute in contour element: %s" % attr)
    identifier = contour.get("identifier")
    if identifier is not None:
        if validate:
            if identifier in identifiers:
                raise GlifLibError(
                    "The identifier %s is used more than once." % identifier
                )
            if not identifierValidator(identifier):
                raise GlifLibError(
                    "The contour identifier %s is not valid." % identifier
                )
        identifiers.add(identifier)
    try:
        pen.beginPath(identifier=identifier)
    except TypeError:
        pen.beginPath()
        warn(
            "The beginPath method needs an identifier kwarg. The contour's identifier value has been discarded.",
            DeprecationWarning,
        )
    if len(contour):
        massaged = _validateAndMassagePointStructures(
            contour, pointAttributesFormat2, validate=validate
        )
        _buildOutlinePointsFormat2(pen, massaged, identifiers, validate)
    pen.endPath()

