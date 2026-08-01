
def test_complex_dispatch_realpart():
    # Test that the real parts of loggamma and gammaln agree on the
    # real axis.
    x = np.r_[-np.logspace(10, -10), np.logspace(-10, 10)] + 0.5

    dataset = np.vstack((x, gammaln(x))).T

    def f(z):
        z = np.array(z, dtype='complex128')
        return loggamma(z).real

    FuncData(f, dataset, 0, 1, rtol=1e-14, atol=1e-14).check()

