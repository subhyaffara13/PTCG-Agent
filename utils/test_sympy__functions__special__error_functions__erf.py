
def test_sympy__functions__special__error_functions__erf():
    from sympy.functions.special.error_functions import erf
    assert _test_args(erf(2))

