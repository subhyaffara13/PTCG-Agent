
def test_sympy__vector__parametricregion__ParametricRegion():
    from sympy.abc import t
    from sympy.vector.parametricregion import ParametricRegion
    assert _test_args(ParametricRegion((t, t**3), (t, 0, 2)))

