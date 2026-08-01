
def test_sympy__codegen__fnodes__Program():
    from sympy.codegen.fnodes import Program
    assert _test_args(Program('foobar', []))

