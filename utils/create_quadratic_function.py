
def create_quadratic_function(n, m, rng):
    a = rng.rand(m)
    A = rng.rand(m, n)
    H = rng.rand(m, n, n)
    HT = np.transpose(H, (1, 2, 0))

    def fun(x):
        return a + A.dot(x) + 0.5 * H.dot(x).dot(x)

    def jac(x):
        return A + H.dot(x)

    def hess(x, v):
        return HT.dot(v)

    return fun, jac, hess

