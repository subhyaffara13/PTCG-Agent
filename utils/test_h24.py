
def test_H24():
    phi = AlgebraicNumber(S.GoldenRatio.expand(func=True), alias='phi')
    assert factor(x**4 - 3*x**2 + 1, extension=phi) == \
        (x - phi)*(x + 1 - phi)*(x - 1 + phi)*(x + phi)

