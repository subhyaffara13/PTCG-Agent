
def test_sympy__functions__special__spherical_harmonics__Ynm():
    from sympy.functions.special.spherical_harmonics import Ynm
    assert _test_args(Ynm(1, 1, x, y))

