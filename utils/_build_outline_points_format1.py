
def _buildOutlinePointsFormat1(
    pen: AbstractPointPen, contour: list[dict[str, Any]]
) -> None:
    for point in contour:
        x = point["x"]
        y = point["y"]
        segmentType = point["segmentType"]
        smooth = point["smooth"]
        name = point["name"]
        pen.addPoint((x, y), segmentType=segmentType, smooth=smooth, name=name)

