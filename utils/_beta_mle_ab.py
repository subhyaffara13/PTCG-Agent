
def _beta_mle_ab(theta, n, s1, s2):
    # Zeros of this function are critical points of
    # the maximum likelihood function.  Solving this system
    # for theta (which contains a and b) gives the MLE for a and b
    # given `n`, `s1` and `s2`.  `s1` is the sum of the logs of the data,
    # and `s2` is the sum of the logs of 1 - data.  `n` is the number
    # of data points.
    a, b = theta
    psiab = sc.psi(a + b)
    func = [s1 - n * (-psiab + sc.psi(a)),
            s2 - n * (-psiab + sc.psi(b))]
    return func

