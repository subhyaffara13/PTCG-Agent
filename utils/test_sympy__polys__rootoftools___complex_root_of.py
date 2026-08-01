
def test_sympy__polys__rootoftools__ComplexRootOf():
    from sympy.polys.rootoftools import ComplexRootOf
    assert _test_args(ComplexRootOf(x**3 + x + 1, 0))

