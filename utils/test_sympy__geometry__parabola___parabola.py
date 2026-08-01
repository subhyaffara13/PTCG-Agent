
def test_sympy__geometry__parabola__Parabola():
    from sympy.geometry.parabola import Parabola
    from sympy.geometry.line import Line
    assert _test_args(Parabola((0, 0), Line((2, 3), (4, 3))))

