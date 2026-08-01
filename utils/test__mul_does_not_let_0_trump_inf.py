
def test_Mul_does_not_let_0_trump_inf():
    assert Mul(*[0, a + zoo]) is S.NaN
    assert Mul(*[0, a + oo]) is S.NaN
    assert Mul(*[0, a + Integral(1/x**2, (x, 1, oo))]) is S.Zero
    # Integral is treated like an unknown like 0*x -> 0
    assert Mul(*[0, a + Integral(x, (x, 1, oo))]) is S.Zero

