
def test_sympy__core__add__Add():
    from sympy.core.add import Add
    assert _test_args(Add(x, y, z, 2))

