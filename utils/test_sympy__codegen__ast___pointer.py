
def test_sympy__codegen__ast__Pointer():
    from sympy.codegen.ast import Pointer, Type, pointer_const
    assert _test_args(Pointer(x))
    assert _test_args(Pointer(y, type=Type('float32')))
    assert _test_args(Pointer(z, Type('float64'), {pointer_const}))

