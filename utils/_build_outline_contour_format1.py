
def _buildOutlineContourFormat1(
    pen: AbstractPointPen, contour: ElementType, validate: bool
) -> None:
    if validate and contour.attrib:
        raise GlifLibError("Unknown attributes in contour element.")
    pen.beginPath()
    if len(contour):
        massaged = _validateAndMassagePointStructures(
            contour,
            pointAttributesFormat1,
            openContourOffCurveLeniency=True,
            validate=validate,
        )
        _buildOutlinePointsFormat1(pen, massaged)
    pen.endPath()

