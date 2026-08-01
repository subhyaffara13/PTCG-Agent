
def test_21494():
    from sympy.testing.pytest import warns_deprecated_sympy

    with warns_deprecated_sympy():
        assert x.expr_free_symbols == {x}

    with warns_deprecated_sympy():
        assert Basic().expr_free_symbols == set()

    with warns_deprecated_sympy():
        assert S(2).expr_free_symbols == {S(2)}

    with warns_deprecated_sympy():
        assert Indexed("A", x).expr_free_symbols == {Indexed("A", x)}

    with warns_deprecated_sympy():
        assert Subs(x, x, 0).expr_free_symbols == set()

