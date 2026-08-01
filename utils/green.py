
def green(t: str) -> str:
    return _c(_GREEN, t)


def green(f, curveXY):
    f = -sp.integrate(sp.sympify(f), y)
    f = f.subs({x: curveXY[0], y: curveXY[1]})
    f = sp.integrate(f * sp.diff(curveXY[0], t), (t, 0, 1))
    return f

