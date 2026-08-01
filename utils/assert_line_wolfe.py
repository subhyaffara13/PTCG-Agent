
def assert_line_wolfe(x, p, s, f, fprime, **kw):
    assert_wolfe(s, phi=lambda sp: f(x + p*sp),
                 derphi=lambda sp: np.dot(fprime(x + p*sp), p), **kw)

