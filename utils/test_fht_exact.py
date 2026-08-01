
def test_fht_exact(n, xp):
    rng = np.random.RandomState(3491349965)

    # for a(r) a power law r^\gamma, the fast Hankel transform produces the
    # exact continuous Hankel transform if biased with q = \gamma

    mu = rng.uniform(0, 3)

    # convergence of HT: -1-mu < gamma < 1/2
    gamma = rng.uniform(-1-mu, 1/2)

    r = np.logspace(-2, 2, n)
    a = xp.asarray(r**gamma)

    dln = math.log(r[1]/r[0])

    offset = fhtoffset(dln, mu, initial=0.0, bias=gamma)
    # offset is a np.float64, which array-api-strict disallows
    # even if it's technically a subclass of float
    offset = float(offset)

    A = fht(a, dln, mu, offset=offset, bias=gamma)

    k = np.exp(offset)/r[::-1]

    # analytical result
    At = xp.asarray((2/k)**gamma * poch((mu+1-gamma)/2, gamma))

    xp_assert_close(A, At)

