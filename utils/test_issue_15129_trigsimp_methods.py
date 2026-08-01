
def test_issue_15129_trigsimp_methods():
    t1 = Matrix([sin(Rational(1, 50)), cos(Rational(1, 50)), 0])
    t2 = Matrix([sin(Rational(1, 25)), cos(Rational(1, 25)), 0])
    t3 = Matrix([cos(Rational(1, 25)), sin(Rational(1, 25)), 0])
    r1 = t1.dot(t2)
    r2 = t1.dot(t3)
    assert trigsimp(r1) == cos(Rational(1, 50))
    assert trigsimp(r2) == sin(Rational(3, 50))

