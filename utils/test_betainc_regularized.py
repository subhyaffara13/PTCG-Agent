
def test_betainc_regularized():
    a, b, x1, x2 = symbols('a b x1 x2')

    assert unchanged(betainc_regularized, a, b, x1, x2)
    assert unchanged(betainc_regularized, a, b, 0, x1)

    assert betainc_regularized(3, 5, 0, -1).is_real == True
    assert betainc_regularized(3, 5, 0, x2).is_real is None
    assert conjugate(betainc_regularized(3*I, 1, 2 + I, 1 + 2*I)) == betainc_regularized(-3*I, 1, 2 - I, 1 - 2*I)

    assert betainc_regularized(a, b, 0, 1).rewrite(Integral) == 1
    assert betainc_regularized(1, 2, x1, x2).rewrite(hyper) == 2*x2*hyper((1, -1), (2,), x2) - 2*x1*hyper((1, -1), (2,), x1)

    assert betainc_regularized(4, 1, 5, 5).evalf() == 0

