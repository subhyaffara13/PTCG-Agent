
def test_sympy__functions__special__error_functions__erfc():
    from sympy.functions.special.error_functions import erfc
    assert _test_args(erfc(2))

