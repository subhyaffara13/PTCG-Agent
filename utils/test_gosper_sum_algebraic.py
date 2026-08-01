
def test_gosper_sum_algebraic():
    assert gosper_sum(
        n**2 + sqrt(2), (n, 0, m)) == (m + 1)*(2*m**2 + m + 6*sqrt(2))/6

