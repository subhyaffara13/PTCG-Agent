
def test_betainc():
    a, b, x1, x2 = symbols('a b x1 x2')

    assert unchanged(betainc, a, b, x1, x2)
    assert unchanged(betainc, a, b, 0, x1)

    assert betainc(1, 2, 0, -5).is_real == True
    assert betainc(1, 2, 0, x2).is_real is None
    assert conjugate(betainc(I, 2, 3 - I, 1 + 4*I)) == betainc(-I, 2, 3 + I, 1 - 4*I)

    assert betainc(a, b, 0, 1).rewrite(Integral).dummy_eq(beta(a, b).rewrite(Integral))
    assert betainc(1, 2, 0, x2).rewrite(hyper) == x2*hyper((1, -1), (2,), x2)

    assert betainc(1, 2, 3, 3).evalf() == 0

