
def _swilk(y, *, xp):
    # calculate Shapiro-Wilk statistic and p-value from sorted sample
    n = y.shape[-1]

    if n == 3:
        # [2] Table 5 gives the first four digits
        c = math.sqrt(2) / 2
        a = xp.asarray([-c, 0, c])
        # [2] Corollary 4; discussed in https://github.com/scipy/scipy/issues/18322
        W = xp.clip(_swilk_w(y, a, xp=xp), 0.75, 1.)
        pvalue = xp.clip(1. - 6/np.pi * xp.acos(xp.sqrt(W)), 0., 1.)
        return W, pvalue

    # Follows [4] section 2.2
    # could calculate half the coefficients and get the rest by antisymmetry
    i = xp.arange(1, n + 1, dtype=y.dtype)
    m = special.ndtri((i - 3 / 8) / (n + 1 / 4))
    u = n**(-0.5)
    mTm = xp.vecdot(m, m)
    c = mTm**(-0.5) * m
    mnm1, mn = m[..., -2], m[..., -1]
    cnm1, cn = c[..., -2], c[..., -1]
    an = (cn + 0.221157*u - 0.147981*u**2
          - 2.071190*u**3 + 4.434685*u**4 - 2.706056*u**5)
    anm1 = (cnm1 + 0.042981*u - 0.293762*u**2
            - 1.752461*u**3 + 5.682633*u**4 - 3.582633*u**5)
    phi = ((mTm - 2*mn**2) / (1 - 2*an**2) if n <= 5
           else (mTm - 2*mn**2 - 2*mnm1**2) / (1 - 2*an**2 - 2*anm1**2))
    a = phi**(-0.5) * m
    if n > 5:
        a = xpx.at(a)[..., -2].set(anm1)
        a = xpx.at(a)[..., 1].set(-anm1)
    a = xpx.at(a)[..., -1].set(an)
    a = xpx.at(a)[..., -0].set(-an)
    W = _swilk_w(y, a, xp=xp)

    # Follows [4] Table 1
    if n <= 11:
        u = n
        gamma = -2.273 + 0.459*u
        mu = 0.5440 - 0.39978*u + 0.025054*u**2 - 0.0006714*u**3
        sigma = math.exp(1.3822 - 0.77857*u + 0.062767*u**2 - 0.0020322*u**3)
        gW = -xp.log(gamma - xp.log(1 - W))
    else:
        u = math.log(n)
        mu = -1.5861 - 0.31082*u - 0.083751*u**2 + 0.0038915*u**3
        sigma = math.exp(-0.4803 - 0.082676*u + 0.0030302*u**2)
        gW = xp.log(1 - W)

    z = (gW - mu) / sigma
    pvalue = special.ndtr(-z)
    return W, pvalue

