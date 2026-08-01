
def test_sympy__functions__special__error_functions__erfs():
    from sympy.functions.special.error_functions import _erfs
    assert _test_args(_erfs(2))

