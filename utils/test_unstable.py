import random

def test_unstable():
    # this is a "Gaussian Toeplitz matrix", as mentioned in Example 2 of
    # I. Gohbert, T. Kailath and V. Olshevsky "Fast Gaussian Elimination with
    # Partial Pivoting for Matrices with Displacement Structure"
    # Mathematics of Computation, 64, 212 (1995), pp 1557-1576
    # which can be unstable for levinson recursion.

    # other fast toeplitz solvers such as GKO or Burg should be better.
    random = np.random.RandomState(1234)
    n = 100
    c = 0.9 ** (np.arange(n)**2)
    y = random.randn(n)

    solution1 = solve_toeplitz(c, b=y)
    solution2 = solve(toeplitz(c), y)

    assert_allclose(solution1, solution2)

