
def test_sympy__codegen__fnodes__ArrayConstructor():
    from sympy.codegen.fnodes import ArrayConstructor
    assert _test_args(ArrayConstructor([1, 2, 3]))
    from sympy.codegen.fnodes import ImpliedDoLoop
    idl = ImpliedDoLoop('i', 'i', 1, 42)
    assert _test_args(ArrayConstructor([1, idl, 3]))

