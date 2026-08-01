
def test_sympy__codegen__cnodes__struct():
    from sympy.codegen.ast import real, Variable
    from sympy.codegen.cnodes import struct
    assert _test_args(struct(declarations=[
        Variable(x, type=real),
        Variable(y, type=real)
    ]))

