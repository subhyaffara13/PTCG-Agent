
def calcCubicPointsC(a, b, c, d):
    p2 = c * (1 / 3) + d
    p3 = (b + c) * (1 / 3) + p2
    p4 = a + b + c + d
    return (d, p2, p3, p4)

