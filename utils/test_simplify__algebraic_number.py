
def test_simplify_AlgebraicNumber():
    A = AlgebraicNumber
    e = 3**(S.One/6)*(3 + (135 + 78*sqrt(3))**Rational(2, 3))/(45 + 26*sqrt(3))**(S.One/3)
    assert simplify(A(e)) == A(12)  # wester test_C20

    e = (41 + 29*sqrt(2))**(S.One/5)
    assert simplify(A(e)) == A(1 + sqrt(2))  # wester test_C21

    e = (3 + 4*I)**Rational(3, 2)
    assert simplify(A(e)) == A(2 + 11*I)  # issue 4401

