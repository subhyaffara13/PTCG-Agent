
def dotest(s):
    for xo in all_objs:
        for yo in all_objs:
            s(xo, yo)
    return True


def dotest(s):
    x = Symbol("x")
    y = Symbol("y")
    l = [
        Rational(2),
        Float("1.3"),
        x,
        y,
        pow(x, y)*y,
        5,
        5.5
    ]
    for x in l:
        for y in l:
            s(x, y)
    return True

