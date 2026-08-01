
def test_C20():
    inside = (135 + 78*sqrt(3))
    test = AlgebraicNumber((inside**R(2, 3) + 3) * sqrt(3) / inside**R(1, 3))
    assert simplify(test) == AlgebraicNumber(12)

