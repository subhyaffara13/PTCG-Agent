
def test_sympy__functions__special__tensor_functions__KroneckerDelta():
    from sympy.functions.special.tensor_functions import KroneckerDelta
    assert _test_args(KroneckerDelta(x, y))

