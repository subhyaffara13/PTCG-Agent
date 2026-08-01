
def test_issue_18770():
    numpy = import_module('numpy')
    if not numpy:
        skip("numpy not installed.")

    from sympy.functions.elementary.miscellaneous import (Max, Min)
    from sympy.utilities.lambdify import lambdify

    expr1 = Min(0.1*x + 3, x + 1, 0.5*x + 1)
    func = lambdify(x, expr1, "numpy")
    assert (func(numpy.linspace(0, 3, 3)) == [1.0, 1.75, 2.5 ]).all()
    assert  func(4) == 3

    expr1 = Max(x**2, x**3)
    func = lambdify(x,expr1, "numpy")
    assert (func(numpy.linspace(-1, 2, 4)) == [1, 0, 1, 8] ).all()
    assert func(4) == 64

