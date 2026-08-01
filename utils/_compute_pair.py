
def _compute_pair(k, h0, xp):
    # Compute the abscissa-weight pairs for each level k. See [1] page 9.

    # For now, we compute and store in 64-bit precision. If higher-precision
    # data types become better supported, it would be good to compute these
    # using the highest precision available. Or, once there is an Array API-
    # compatible arbitrary precision array, we can compute at the required
    # precision.

    # "....each level k of abscissa-weight pairs uses h = 2 **-k"
    # We adapt to floating point arithmetic using ideas of [2].
    h = h0 / 2**k
    max = _N_BASE_STEPS * 2**k

    # For iterations after the first, "....the integrand function needs to be
    # evaluated only at the odd-indexed abscissas at each level."
    j = xp.arange(max+1) if k == 0 else xp.arange(1, max+1, 2)
    jh = j * h

    # "In this case... the weights wj = u1/cosh(u2)^2, where..."
    pi_2 = xp.pi / 2
    u1 = pi_2*xp.cosh(jh)
    u2 = pi_2*xp.sinh(jh)
    # Denominators get big here. Overflow then underflow doesn't need warning.
    # with np.errstate(under='ignore', over='ignore'):
    wj = u1 / xp.cosh(u2)**2
    # "We actually store 1-xj = 1/(...)."
    xjc = 1 / (xp.exp(u2) * xp.cosh(u2))  # complement of xj = xp.tanh(u2)

    # When level k == 0, the zeroth xj corresponds with xj = 0. To simplify
    # code, the function will be evaluated there twice; each gets half weight.
    wj[0] = wj[0] / 2 if k == 0 else wj[0]

    return xjc, wj  # store at full precision

