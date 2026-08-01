
def test_Normal():
    m = Normal('A', [1, 2], [[1, 0], [0, 1]])
    A = MultivariateNormal('A', [1, 2], [[1, 0], [0, 1]])
    assert m == A
    assert density(m)(1, 2) == 1/(2*pi)
    assert m.pspace.distribution.set == ProductSet(S.Reals, S.Reals)
    raises (ValueError, lambda:m[2])
    n = Normal('B', [1, 2, 3], [[1, 0, 0], [0, 1, 0], [0, 0, 1]])
    p = Normal('C',  Matrix([1, 2]), Matrix([[1, 0], [0, 1]]))
    assert density(m)(x, y) == density(p)(x, y)
    assert marginal_distribution(n, 0, 1)(1, 2) == 1/(2*pi)
    raises(ValueError, lambda: marginal_distribution(m))
    assert integrate(density(m)(x, y), (x, -oo, oo), (y, -oo, oo)).evalf() == 1.0
    N = Normal('N', [1, 2], [[x, 0], [0, y]])
    assert density(N)(0, 0) == exp(-((4*x + y)/(2*x*y)))/(2*pi*sqrt(x*y))

    raises (ValueError, lambda: Normal('M', [1, 2], [[1, 1], [1, -1]]))
    # symbolic
    n = symbols('n', integer=True, positive=True)
    mu = MatrixSymbol('mu', n, 1)
    sigma = MatrixSymbol('sigma', n, n)
    X = Normal('X', mu, sigma)
    assert density(X) == MultivariateNormalDistribution(mu, sigma)
    raises (NotImplementedError, lambda: median(m))
    # Below tests should work after issue #17267 is resolved
    # assert E(X) == mu
    # assert variance(X) == sigma

    # test symbolic multivariate normal densities
    n = 3

    Sg = MatrixSymbol('Sg', n, n)
    mu = MatrixSymbol('mu', n, 1)
    obs = MatrixSymbol('obs', n, 1)

    X = MultivariateNormal('X', mu, Sg)
    density_X = density(X)

    eval_a = density_X(obs).subs({Sg: eye(3),
        mu: Matrix([0, 0, 0]), obs: Matrix([0, 0, 0])}).doit()
    eval_b = density_X(0, 0, 0).subs({Sg: eye(3), mu: Matrix([0, 0, 0])}).doit()

    assert eval_a == sqrt(2)/(4*pi**Rational(3/2))
    assert eval_b == sqrt(2)/(4*pi**Rational(3/2))

    n = symbols('n', integer=True, positive=True)

    Sg = MatrixSymbol('Sg', n, n)
    mu = MatrixSymbol('mu', n, 1)
    obs = MatrixSymbol('obs', n, 1)

    X = MultivariateNormal('X', mu, Sg)
    density_X_at_obs = density(X)(obs)

    expected_density = MatrixElement(
        exp((S(1)/2) * (mu.T - obs.T) * Sg**(-1) * (-mu + obs)) / \
        sqrt((2*pi)**n * Determinant(Sg)), 0, 0)

    assert density_X_at_obs == expected_density

