
def test_minres_precond_exact_x0():
    rng = np.random.RandomState(1234)
    rtol = 1e-6
    a = np.eye(10)
    b = np.ones(10)
    c = np.ones(10)
    m = rng.randn(10, 10)
    m = np.dot(m, m.T)
    x = minres(a, b, M=m, x0=c, rtol=rtol)[0]
    assert norm(a @ x - b) <= rtol * norm(b)

