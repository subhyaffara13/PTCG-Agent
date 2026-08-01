
def test_sympy__functions__special__gamma_functions__trigamma():
    from sympy.functions.special.gamma_functions import trigamma
    assert _test_args(trigamma(x))

