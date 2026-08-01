
def test_sympy__codegen__fnodes__use_rename():
    from sympy.codegen.fnodes import use_rename
    assert _test_args(use_rename('loc', 'glob'))

