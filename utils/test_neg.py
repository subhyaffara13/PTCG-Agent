
def test_neg():
    assert -SeqPer((1, -2), (n, 0, oo)) == SeqPer((-1, 2), (n, 0, oo))
    assert -SeqFormula(n**2) == SeqFormula(-n**2)


def test_neg():
    n = ArithmeticOnlyMatrix(1, 2, [1, 2])
    assert -n == ArithmeticOnlyMatrix(1, 2, [-1, -2])


def test_neg():
    n = Matrix(1, 2, [1, 2])
    assert -n == Matrix(1, 2, [-1, -2])

