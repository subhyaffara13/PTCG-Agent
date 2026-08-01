
def test_sympy__functions__special__spherical_harmonics__Znm():
    from sympy.functions.special.spherical_harmonics import Znm
    assert _test_args(Znm(x, y, 1, 1))

