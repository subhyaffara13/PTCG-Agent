
def test_sympy__codegen__fnodes__SubroutineCall():
    from sympy.codegen.fnodes import SubroutineCall
    assert _test_args(SubroutineCall('foo', ['bar', 'baz']))

