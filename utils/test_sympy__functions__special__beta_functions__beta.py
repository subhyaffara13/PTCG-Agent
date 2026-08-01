
def test_sympy__functions__special__beta_functions__beta():
    from sympy.functions.special.beta_functions import beta
    assert _test_args(beta(x))
    assert _test_args(beta(x, x))

