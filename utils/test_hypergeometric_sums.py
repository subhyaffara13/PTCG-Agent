
def test_hypergeometric_sums():
    assert summation(
        binomial(2*k, k)/4**k, (k, 0, n)) == (1 + 2*n)*binomial(2*n, n)/4**n
    assert summation(binomial(2*k, k)/5**k, (k, -oo, oo)) == sqrt(5)

