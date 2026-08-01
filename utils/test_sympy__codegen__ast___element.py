
def test_sympy__codegen__ast__Element():
    from sympy.codegen.ast import Element
    assert _test_args(Element('x', range(3)))

