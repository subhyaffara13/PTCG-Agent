
def test_sympy__functions__special__gamma_functions__polygamma():
    from sympy.functions.special.gamma_functions import polygamma
    assert _test_args(polygamma(x, 2))

