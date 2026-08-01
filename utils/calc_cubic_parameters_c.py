
def calcCubicParametersC(pt1, pt2, pt3, pt4):
    c = (pt2 - pt1) * 3.0
    b = (pt3 - pt2) * 3.0 - c
    a = pt4 - pt1 - c - b
    return (a, b, c, pt1)

