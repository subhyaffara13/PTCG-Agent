
def test_sympy__functions__special__error_functions__fresnels():
    from sympy.functions.special.error_functions import fresnels
    assert _test_args(fresnels(2))

