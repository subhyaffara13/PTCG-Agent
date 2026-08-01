
def _buildOutlinePointsFormat2(
    pen: AbstractPointPen,
    contour: list[dict[str, Any]],
    identifiers: set[str],
    validate: bool,
) -> None:
    for point in contour:
        x = point["x"]
        y = point["y"]
        segmentType = point["segmentType"]
        smooth = point["smooth"]
        name = point["name"]
        identifier = point.get("identifier")
        if identifier is not None:
            if validate:
                if identifier in identifiers:
                    raise GlifLibError(
                        "The identifier %s is used more than once." % identifier
                    )
                if not identifierValidator(identifier):
                    raise GlifLibError("The identifier %s is not valid." % identifier)
            identifiers.add(identifier)
        try:
            pen.addPoint(
                (x, y),
                segmentType=segmentType,
                smooth=smooth,
                name=name,
                identifier=identifier,
            )
        except TypeError:
            pen.addPoint((x, y), segmentType=segmentType, smooth=smooth, name=name)
            warn(
                "The addPoint method needs an identifier kwarg. The point's identifier value has been discarded.",
                DeprecationWarning,
            )

