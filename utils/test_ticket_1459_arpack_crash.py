
def test_ticket_1459_arpack_crash():
    for dtype in [np.float32, np.float64]:
        # This test does not seem to catch the issue for float32,
        # but we made the same fix there, just to be sure

        N = 6
        k = 2

        np.random.seed(2301)
        A = np.random.random((N, N)).astype(dtype)
        v0 = np.array([-0.71063568258907849895, -0.83185111795729227424,
                       -0.34365925382227402451, 0.46122533684552280420,
                       -0.58001341115969040629, -0.78844877570084292984e-01],
                      dtype=dtype)

        # Should not crash:
        evals, evecs = eigs(A, k, v0=v0)

