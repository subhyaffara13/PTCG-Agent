
def test_gh24358(dtype):
    # gh-24358: eigs with which="SR" returned zeros due to nev variable was modifed
    #  after naupd calls in the C ARPACK implementation. This was due to hitting a
    # complex valued eig but requesting only one of them.

    # Test the specific issue in gh-24358
    A = csr_array(np.array([[-1.3, 2.7, 0.2],
                            [0.8, 4.1, 2.2],
                            [2.1, 4.4, -1.9]], dtype=dtype))
    w, z = eigs(A, 1, which="SR")
    atol = 1e-4 if dtype in [np.float32, np.complex64] else 1e-6
    assert_allclose(w.real, -2.495689365014214, atol=atol, rtol=0.0)
    # ARPACK can sometimes pick up the conjugate
    assert_allclose(np.abs(w.imag), 0.5173365219668336, atol=atol, rtol=0.0)
    assert_allclose(A @ z, w * z, atol=atol, rtol=0.0)

