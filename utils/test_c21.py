
def test_C21():
    assert simplify(AlgebraicNumber((41 + 29*sqrt(2)) ** R(1, 5))) == \
        AlgebraicNumber(1 + sqrt(2))

