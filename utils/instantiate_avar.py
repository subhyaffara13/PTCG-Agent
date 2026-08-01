
def instantiateAvar(varfont, axisLimits):
    # 'axisLimits' dict must contain user-space (non-normalized) coordinates.

    avar = varfont["avar"]

    segments = avar.segments

    # drop table if we instantiate all the axes
    pinnedAxes = set(axisLimits.pinnedLocation())
    if pinnedAxes.issuperset(segments):
        log.info("Dropping avar table")
        del varfont["avar"]
        return

    if getattr(avar, "majorVersion", 1) >= 2 and avar.table.VarStore:
        raise NotImplementedError("avar table with VarStore is not supported")

    log.info("Instantiating avar table")
    for axis in pinnedAxes:
        if axis in segments:
            del segments[axis]

    # First compute the default normalization for axisLimits coordinates: i.e.
    # min = -1.0, default = 0, max = +1.0, and in between values interpolated linearly,
    # without using the avar table's mappings.
    # Then, for each SegmentMap, if we are restricting its axis, compute the new
    # mappings by dividing the key/value pairs by the desired new min/max values,
    # dropping any mappings that fall outside the restricted range.
    # The keys ('fromCoord') are specified in default normalized coordinate space,
    # whereas the values ('toCoord') are "mapped forward" using the SegmentMap.
    normalizedRanges = axisLimits.normalize(varfont, usingAvar=False)
    newSegments = {}
    for axisTag, mapping in segments.items():
        if not _isValidAvarSegmentMap(axisTag, mapping):
            continue
        if mapping and axisTag in normalizedRanges:
            axisRange = normalizedRanges[axisTag]
            mappedMin = floatToFixedToFloat(
                piecewiseLinearMap(axisRange.minimum, mapping), 14
            )
            mappedDef = floatToFixedToFloat(
                piecewiseLinearMap(axisRange.default, mapping), 14
            )
            mappedMax = floatToFixedToFloat(
                piecewiseLinearMap(axisRange.maximum, mapping), 14
            )
            mappedAxisLimit = NormalizedAxisTripleAndDistances(
                mappedMin,
                mappedDef,
                mappedMax,
                axisRange.distanceNegative,
                axisRange.distancePositive,
            )
            newMapping = {}
            for fromCoord, toCoord in mapping.items():
                if fromCoord < axisRange.minimum or fromCoord > axisRange.maximum:
                    continue
                fromCoord = axisRange.renormalizeValue(fromCoord)

                assert mappedMin <= toCoord <= mappedMax
                toCoord = mappedAxisLimit.renormalizeValue(toCoord)

                fromCoord = floatToFixedToFloat(fromCoord, 14)
                toCoord = floatToFixedToFloat(toCoord, 14)
                newMapping[fromCoord] = toCoord
            newMapping.update({-1.0: -1.0, 0.0: 0.0, 1.0: 1.0})
            newSegments[axisTag] = newMapping
        else:
            newSegments[axisTag] = mapping
    avar.segments = newSegments

