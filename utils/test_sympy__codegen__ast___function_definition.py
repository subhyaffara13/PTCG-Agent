
def test_sympy__codegen__ast__FunctionDefinition():
    from sympy.codegen.ast import FunctionDefinition, real, Declaration, Variable, Assignment
    inp_x = Declaration(Variable(x, type=real))
    assert _test_args(FunctionDefinition(real, 'pwer', [inp_x], [Assignment(x, x**2)]))

