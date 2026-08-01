
def test_sympy__functions__special__error_functions__erfi():
    from sympy.functions.special.error_functions import erfi
    assert _test_args(erfi(2))

