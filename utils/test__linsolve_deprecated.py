
def test__linsolve_deprecated():
    raises(PolyNonlinearError, lambda:
        _linsolve([Eq(x**2, x**2 + y)], [x, y]))
    raises(PolyNonlinearError, lambda:
        _linsolve([(x + y)**2 - x**2], [x]))
    raises(PolyNonlinearError, lambda:
        _linsolve([Eq((x + y)**2, x**2)], [x]))

