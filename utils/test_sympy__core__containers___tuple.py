
def test_sympy__core__containers__Tuple():
    from sympy.core.containers import Tuple
    assert _test_args(Tuple(x, y, z, 2))

