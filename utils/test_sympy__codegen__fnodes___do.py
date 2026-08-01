
def test_sympy__codegen__fnodes__Do():
    from sympy.codegen.fnodes import Do
    assert _test_args(Do([], 'i', 1, 42))

