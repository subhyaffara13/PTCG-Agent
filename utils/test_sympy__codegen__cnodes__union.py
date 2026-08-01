
def test_sympy__codegen__cnodes__union():
    from sympy.codegen.ast import float32, int32, Variable
    from sympy.codegen.cnodes import union
    assert _test_args(union(declarations=[
        Variable(x, type=float32),
        Variable(y, type=int32)
    ]))

