
def test_sympy__codegen__ast__FunctionPrototype():
    from sympy.codegen.ast import FunctionPrototype, real, Declaration, Variable
    inp_x = Declaration(Variable(x, type=real))
    assert _test_args(FunctionPrototype(real, 'pwer', [inp_x]))

