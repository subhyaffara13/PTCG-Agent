
def test_sympy__codegen__fnodes__Extent():
    from sympy.codegen.fnodes import Extent
    assert _test_args(Extent())
    assert _test_args(Extent(None))
    assert _test_args(Extent(':'))
    assert _test_args(Extent(-3, 4))
    assert _test_args(Extent(x, y))

