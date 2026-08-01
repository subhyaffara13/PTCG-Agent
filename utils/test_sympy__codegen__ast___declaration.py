
def test_sympy__codegen__ast__Declaration():
    from sympy.codegen.ast import Declaration, Variable, Type
    vx = Variable(x, type=Type('float'))
    assert _test_args(Declaration(vx))

