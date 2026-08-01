
def test_product_spaces():
    X1 = Geometric('X1', S.Half)
    X2 = Geometric('X2', Rational(1, 3))
    assert str(P(X1 + X2 < 3).rewrite(Sum)) == (
        "Sum(Piecewise((1/(4*2**n), n >= -1), (0, True)), (n, -oo, -1))/3")
    assert str(P(X1 + X2 > 3).rewrite(Sum)) == (
        'Sum(Piecewise((2**(X2 - n - 2)*(2/3)**(X2 - 1)/6, '
        'X2 - n <= 2), (0, True)), (X2, 1, oo), (n, 1, oo))')
    assert P(Eq(X1 + X2, 3)) == Rational(1, 12)

