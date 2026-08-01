
def test_sympy__functions__special__error_functions__expint():
    from sympy.functions.special.error_functions import expint
    assert _test_args(expint(y, x))

