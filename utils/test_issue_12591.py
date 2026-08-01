
def test_issue_12591():
    x, y = symbols("x y", real=True)
    assert fourier_transform(exp(x), x, y) == FourierTransform(exp(x), x, y)

