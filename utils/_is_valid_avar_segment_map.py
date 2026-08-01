
def _isValidAvarSegmentMap(axisTag, segmentMap):
    if not segmentMap:
        return True
    if not {(-1.0, -1.0), (0, 0), (1.0, 1.0)}.issubset(segmentMap.items()):
        log.warning(
            f"Invalid avar SegmentMap record for axis '{axisTag}': does not "
            "include all required value maps {-1.0: -1.0, 0: 0, 1.0: 1.0}"
        )
        return False
    previousValue = None
    for fromCoord, toCoord in sorted(segmentMap.items()):
        if previousValue is not None and previousValue > toCoord:
            log.warning(
                f"Invalid avar AxisValueMap({fromCoord}, {toCoord}) record "
                f"for axis '{axisTag}': the toCoordinate value must be >= to "
                f"the toCoordinate value of the preceding record ({previousValue})."
            )
            return False
        previousValue = toCoord
    return True

