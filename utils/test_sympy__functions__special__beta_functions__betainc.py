
def test_sympy__functions__special__beta_functions__betainc():
    from sympy.functions.special.beta_functions import betainc
    assert _test_args(betainc(a, b, x, y))

