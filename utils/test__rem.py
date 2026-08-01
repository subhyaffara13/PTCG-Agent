
def test_Rem():
    from sympy.abc import x, y
    assert Rem(5, 3) == 2
    assert Rem(-5, 3) == -2
    assert Rem(5, -3) == 2
    assert Rem(-5, -3) == -2
    assert Rem(x**3, y) == Rem(x**3, y)
    assert Rem(Rem(-5, 3) + 3, 3) == 1

