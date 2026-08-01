
def test_sympy__codegen__cxxnodes__using():
    from sympy.codegen.cxxnodes import using
    assert _test_args(using('std::vector'))
    assert _test_args(using('std::vector', 'vec'))

