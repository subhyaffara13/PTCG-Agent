
def test_sympy__functions__special__zeta_functions__stieltjes():
    from sympy.functions.special.zeta_functions import stieltjes
    assert _test_args(stieltjes(x, y))

