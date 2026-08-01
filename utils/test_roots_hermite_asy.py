
def test_roots_hermite_asy():
    # Recursion for Hermite functions
    def hermite_recursion(n, nodes):
        H = np.zeros((n, nodes.size))
        H[0,:] = np.pi**(-0.25) * np.exp(-0.5*nodes**2)
        if n > 1:
            H[1,:] = sqrt(2.0) * nodes * H[0,:]
            for k in range(2, n):
                H[k,:] = sqrt(2.0/k) * nodes * H[k-1,:] - sqrt((k-1.0)/k) * H[k-2,:]
        return H

    # This tests only the nodes
    def test(N, rtol=1e-15, atol=1e-14):
        x, w = orth._roots_hermite_asy(N)
        H = hermite_recursion(N+1, x)
        assert_allclose(H[-1,:], np.zeros(N), rtol, atol)
        assert_allclose(sum(w), sqrt(np.pi), rtol, atol)

    test(150, atol=1e-12)
    test(151, atol=1e-12)
    test(300, atol=1e-12)
    test(301, atol=1e-12)
    test(500, atol=1e-12)
    test(501, atol=1e-12)
    test(999, atol=1e-12)
    test(1000, atol=1e-12)
    test(2000, atol=1e-12)
    test(5000, atol=1e-12)

