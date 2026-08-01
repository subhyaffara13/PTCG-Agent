
def test_sympy__functions__special__error_functions__erfinv():
    from sympy.functions.special.error_functions import erfinv
    assert _test_args(erfinv(2))

