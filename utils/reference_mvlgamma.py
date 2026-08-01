
def reference_mvlgamma(x, d):
    if x.dtype == np.float16:
        return scipy.special.multigammaln(x, d).astype(np.float16)

    return scipy.special.multigammaln(x, d)

