
def test_sympy__functions__special__zeta_functions__zeta():
    from sympy.functions.special.zeta_functions import zeta
    assert _test_args(zeta(101))

