
def test_ishermitian_approximate_results():
    n = 20
    rng = np.random.RandomState(987654321)
    x = rng.uniform(high=5., size=[n, n])
    y = x @ x.T  # symmetric
    p = rng.standard_normal([n, n]) + rng.standard_normal([n, n])*1j
    z = p @ y @ p.conj().T
    assert ishermitian(z, atol=1e-10)
    assert ishermitian(z, atol=1e-10, rtol=0.)
    assert ishermitian(z, atol=0., rtol=1e-12)
    assert ishermitian(z, atol=1e-13, rtol=1e-12)

