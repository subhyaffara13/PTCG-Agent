
def test_sympy__codegen__fnodes__Module():
    from sympy.codegen.fnodes import Module
    assert _test_args(Module('foobar', [], []))

