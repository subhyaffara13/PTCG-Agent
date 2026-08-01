
def test_rewrite_Add():
    from sympy.testing.pytest import warns_deprecated_sympy
    with warns_deprecated_sympy():
        assert Eq(x, y).rewrite(Add) == x - y

