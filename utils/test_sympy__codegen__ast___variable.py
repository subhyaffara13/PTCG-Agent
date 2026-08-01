
def test_sympy__codegen__ast__Variable():
    from sympy.codegen.ast import Variable, Type, value_const
    assert _test_args(Variable(x))
    assert _test_args(Variable(y, Type('float32'), {value_const}))
    assert _test_args(Variable(z, type=Type('float64')))

