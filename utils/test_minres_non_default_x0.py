
def test_minres_non_default_x0(make_complex):
    rng = np.random.RandomState(1234)
    rtol = 1e-6
    a = rng.randn(5, 5) if not make_complex else rng.randn(5, 5) + 1j * rng.randn(5, 5)
    a = np.dot(a, a.T) if not make_complex else np.dot(a, a.T.conj())
    b = rng.randn(5)
    c = rng.randn(5)
    x = minres(a, b, x0=c, rtol=rtol)[0]
    assert norm(a @ x - b) <= rtol * norm(b)

