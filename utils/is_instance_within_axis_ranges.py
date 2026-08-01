
def isInstanceWithinAxisRanges(location, axisRanges):
    for axisTag, coord in location.items():
        if axisTag in axisRanges:
            axisRange = axisRanges[axisTag]
            if coord < axisRange.minimum or coord > axisRange.maximum:
                return False
    return True

