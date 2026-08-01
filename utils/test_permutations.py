
def test_permutations():
    rng = np.random.default_rng(1234)
    for _ in range(10):
        n = rng.integers(1, 100)
        # Random real/complex array
        x = rng.random((n, n)) + 0 if rng.integers(2) else rng.random((n, n))*1j
        x = x + x.conj().T
        x += eye(n)*rng.integers(5, 1e6)
        l_ind = tril_indices_from(x, k=-1)
        u_ind = triu_indices_from(x, k=1)

        # Test whether permutations lead to a triangular array
        u, d, p = ldl(x, lower=0)
        # lower part should be zero
        assert_(not any(u[p, :][l_ind]), f'Spin {_} failed')

        l, d, p = ldl(x, lower=1)
        # upper part should be zero
        assert_(not any(l[p, :][u_ind]), f'Spin {_} failed')

