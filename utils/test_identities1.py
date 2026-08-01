
def test_identities1():
    # test the identity exp(loggamma(z)) = gamma(z)
    x = np.array([-99.5, -9.5, -0.5, 0.5, 9.5, 99.5])
    y = x.copy()
    x, y = np.meshgrid(x, y)
    z = (x + 1J*y).flatten()
    dataset = np.vstack((z, gamma(z))).T

    def f(z):
        return np.exp(loggamma(z))

    FuncData(f, dataset, 0, 1, rtol=1e-14, atol=1e-14).check()

