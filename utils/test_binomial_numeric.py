
def test_binomial_numeric():
    nvals = range(5)
    pvals = [0, Rational(1, 4), S.Half, Rational(3, 4), 1]

    for n in nvals:
        for p in pvals:
            X = Binomial('X', n, p)
            assert E(X) == n*p
            assert variance(X) == n*p*(1 - p)
            if n > 0 and 0 < p < 1:
                assert skewness(X) == (1 - 2*p)/sqrt(n*p*(1 - p))
                assert kurtosis(X) == 3 + (1 - 6*p*(1 - p))/(n*p*(1 - p))
            for k in range(n + 1):
                assert P(Eq(X, k)) == binomial(n, k)*p**k*(1 - p)**(n - k)

