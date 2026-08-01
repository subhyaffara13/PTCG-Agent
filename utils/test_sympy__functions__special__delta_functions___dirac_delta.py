
def test_sympy__functions__special__delta_functions__DiracDelta():
    from sympy.functions.special.delta_functions import DiracDelta
    assert _test_args(DiracDelta(x, 1))

