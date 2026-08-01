
def check_moment_frozen(distfn, arg, m, k):
    npt.assert_allclose(distfn(*arg).moment(k), m,
                        atol=1e-10, rtol=1e-10)

