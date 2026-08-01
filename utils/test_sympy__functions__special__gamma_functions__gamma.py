
def test_sympy__functions__special__gamma_functions__gamma():
    from sympy.functions.special.gamma_functions import gamma
    assert _test_args(gamma(x))

