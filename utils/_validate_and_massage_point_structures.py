
def _validateAndMassagePointStructures(
    contour, pointAttributes, openContourOffCurveLeniency=False, validate=True
):
    if not len(contour):
        return
    # store some data for later validation
    lastOnCurvePoint = None
    haveOffCurvePoint = False
    # validate and massage the individual point elements
    massaged = []
    for index, element in enumerate(contour):
        # not <point>
        if element.tag != "point":
            raise GlifLibError(
                "Unknown child element (%s) of contour element." % element.tag
            )
        point = dict(element.attrib)
        massaged.append(point)
        if validate:
            # unknown attributes
            for attr in point.keys():
                if attr not in pointAttributes:
                    raise GlifLibError("Unknown attribute in point element: %s" % attr)
            # search for unknown children
            if len(element):
                raise GlifLibError("Unknown child elements in point element.")
        # x and y are required
        for attr in ("x", "y"):
            try:
                point[attr] = _number(point[attr])
            except KeyError as e:
                raise GlifLibError(
                    f"Required {attr} attribute is missing in point element."
                ) from e
        # segment type
        pointType = point.pop("type", "offcurve")
        if validate and pointType not in pointTypeOptions:
            raise GlifLibError("Unknown point type: %s" % pointType)
        if pointType == "offcurve":
            pointType = None
        point["segmentType"] = pointType
        if pointType is None:
            haveOffCurvePoint = True
        else:
            lastOnCurvePoint = index
        # move can only occur as the first point
        if validate and pointType == "move" and index != 0:
            raise GlifLibError(
                "A move point occurs after the first point in the contour."
            )
        # smooth is optional
        smooth = point.get("smooth", "no")
        if validate and smooth is not None:
            if smooth not in pointSmoothOptions:
                raise GlifLibError("Unknown point smooth value: %s" % smooth)
        smooth = smooth == "yes"
        point["smooth"] = smooth
        # smooth can only be applied to curve and qcurve
        if validate and smooth and pointType is None:
            raise GlifLibError("smooth attribute set in an offcurve point.")
        # name is optional
        if "name" not in element.attrib:
            point["name"] = None
    if openContourOffCurveLeniency:
        # remove offcurves that precede a move. this is technically illegal,
        # but we let it slide because there are fonts out there in the wild like this.
        if massaged[0]["segmentType"] == "move":
            count = 0
            for point in reversed(massaged):
                if point["segmentType"] is None:
                    count += 1
                else:
                    break
            if count:
                massaged = massaged[:-count]
    # validate the off-curves in the segments
    if validate and haveOffCurvePoint and lastOnCurvePoint is not None:
        # we only care about how many offCurves there are before an onCurve
        # filter out the trailing offCurves
        offCurvesCount = len(massaged) - 1 - lastOnCurvePoint
        for point in massaged:
            segmentType = point["segmentType"]
            if segmentType is None:
                offCurvesCount += 1
            else:
                if offCurvesCount:
                    # move and line can't be preceded by off-curves
                    if segmentType == "move":
                        # this will have been filtered out already
                        raise GlifLibError("move can not have an offcurve.")
                    elif segmentType == "line":
                        raise GlifLibError("line can not have an offcurve.")
                    elif segmentType == "curve":
                        if offCurvesCount > 2:
                            raise GlifLibError("Too many offcurves defined for curve.")
                    elif segmentType == "qcurve":
                        pass
                    else:
                        # unknown segment type. it'll be caught later.
                        pass
                offCurvesCount = 0
    return massaged

