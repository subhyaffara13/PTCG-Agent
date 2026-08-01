
def very_random_gen(seed=0):
    rng = np.random.default_rng(389234982354865)
    m_eq, m_ub, n = 10, 20, 50
    c = rng.random(n)-0.5
    A_ub = rng.random((m_ub, n))-0.5
    b_ub = rng.random(m_ub)-0.5
    A_eq = rng.random((m_eq, n))-0.5
    b_eq = rng.random(m_eq)-0.5
    lb = -rng.random(n)
    ub = rng.random(n)
    lb[lb < -rng.random()] = -np.inf
    ub[ub > rng.random()] = np.inf
    bounds = np.vstack((lb, ub)).T
    return c, A_ub, b_ub, A_eq, b_eq, bounds

