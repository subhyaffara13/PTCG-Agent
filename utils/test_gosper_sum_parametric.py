
def test_gosper_sum_parametric():
    assert gosper_sum(binomial(S.Half, m - j + 1)*binomial(S.Half, m + j), (j, 1, n)) == \
        n*(1 + m - n)*(-1 + 2*m + 2*n)*binomial(S.Half, 1 + m - n)* \
        binomial(S.Half, m + n)/(m*(1 + 2*m))

