
def _beta_mle_a(a, b, n, s1):
    # The zeros of this function give the MLE for `a`, with
    # `b`, `n` and `s1` given.  `s1` is the sum of the logs of
    # the data. `n` is the number of data points.
    psiab = sc.psi(a + b)
    func = s1 - n * (-psiab + sc.psi(a))
    return func

