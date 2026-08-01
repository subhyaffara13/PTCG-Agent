
def test_H18():
    # Factor over complex rationals.
    test = factor(4*x**4 + 8*x**3 + 77*x**2 + 18*x + 153)
    good = (2*x + 3*I)*(2*x - 3*I)*(x + 1 - 4*I)*(x + 1 + 4*I)
    assert test == good

