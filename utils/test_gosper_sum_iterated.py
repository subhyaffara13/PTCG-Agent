
def test_gosper_sum_iterated():
    f1 = binomial(2*k, k)/4**k
    f2 = (1 + 2*n)*binomial(2*n, n)/4**n
    f3 = (1 + 2*n)*(3 + 2*n)*binomial(2*n, n)/(3*4**n)
    f4 = (1 + 2*n)*(3 + 2*n)*(5 + 2*n)*binomial(2*n, n)/(15*4**n)
    f5 = (1 + 2*n)*(3 + 2*n)*(5 + 2*n)*(7 + 2*n)*binomial(2*n, n)/(105*4**n)

    assert gosper_sum(f1, (k, 0, n)) == f2
    assert gosper_sum(f2, (n, 0, n)) == f3
    assert gosper_sum(f3, (n, 0, n)) == f4
    assert gosper_sum(f4, (n, 0, n)) == f5

