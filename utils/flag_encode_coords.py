
def flagEncodeCoords(flag, x, y, xBytes, yBytes):
    flagEncodeCoord(flag, flagXsame | flagXShort, x, xBytes)
    flagEncodeCoord(flag, flagYsame | flagYShort, y, yBytes)

