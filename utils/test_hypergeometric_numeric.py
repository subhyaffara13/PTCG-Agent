
def test_hypergeometric_numeric():
    for N in range(1, 5):
        for m in range(0, N + 1):
            for n in range(1, N + 1):
                X = Hypergeometric('X', N, m, n)
                N, m, n = map(sympify, (N, m, n))
                assert sum(density(X).values()) == 1
                assert E(X) == n * m / N
                if N > 1:
                    assert variance(X) == n*(m/N)*(N - m)/N*(N - n)/(N - 1)
                # Only test for skewness when defined
                if N > 2 and 0 < m < N and n < N:
                    assert skewness(X) == simplify((N - 2*m)*sqrt(N - 1)*(N - 2*n)
                        / (sqrt(n*m*(N - m)*(N - n))*(N - 2)))

