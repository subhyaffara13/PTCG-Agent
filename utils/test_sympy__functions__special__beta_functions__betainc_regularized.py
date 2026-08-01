
def test_sympy__functions__special__beta_functions__betainc_regularized():
    from sympy.functions.special.beta_functions import betainc_regularized
    assert _test_args(betainc_regularized(a, b, x, y))

