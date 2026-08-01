
def test_sympy__functions__special__gamma_functions__multigamma():
    from sympy.functions.special.gamma_functions import multigamma
    assert _test_args(multigamma(x, 1))

