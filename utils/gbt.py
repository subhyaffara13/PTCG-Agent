
def gbt(tf, sample_per, alpha):
    r"""
    Returns falling coefficients of H(z) from numerator and denominator.

    Explanation
    ===========

    Where H(z) is the corresponding discretized transfer function,
    discretized with the generalised bilinear transformation method.
    H(z) is obtained from the continuous transfer function H(s)
    by substituting $s(z) = \frac{z-1}{T(\alpha z + (1-\alpha))}$ into H(s), where T is the
    sample period.
    Coefficients are falling, i.e. $H(z) = \frac{az+b}{cz+d}$ is returned
    as [a, b], [c, d].

    Examples
    ========

    >>> from sympy.physics.control.lti import TransferFunction, gbt
    >>> from sympy.abc import s, L, R, T

    >>> tf = TransferFunction(1, s*L + R, s)
    >>> numZ, denZ = gbt(tf, T, 0.5)
    >>> numZ
    [T/(2*(L + R*T/2)), T/(2*(L + R*T/2))]
    >>> denZ
    [1, (-L + R*T/2)/(L + R*T/2)]

    >>> numZ, denZ = gbt(tf, T, 0)
    >>> numZ
    [T/L]
    >>> denZ
    [1, (-L + R*T)/L]

    >>> numZ, denZ = gbt(tf, T, 1)
    >>> numZ
    [T/(L + R*T), 0]
    >>> denZ
    [1, -L/(L + R*T)]

    >>> numZ, denZ = gbt(tf, T, 0.3)
    >>> numZ
    [3*T/(10*(L + 3*R*T/10)), 7*T/(10*(L + 3*R*T/10))]
    >>> denZ
    [1, (-L + 7*R*T/10)/(L + 3*R*T/10)]

    References
    ==========

    .. [1] https://www.polyu.edu.hk/ama/profile/gfzhang/Research/ZCC09_IJC.pdf
    """
    if not tf.is_SISO:
        raise NotImplementedError("Not implemented for MIMO systems.")

    T = sample_per  # and sample period T
    s = tf.var
    z =  s         # dummy discrete variable z

    np = tf.num.as_poly(s).all_coeffs()
    dp = tf.den.as_poly(s).all_coeffs()
    alpha = Rational(alpha).limit_denominator(1000)

    # The next line results from multiplying H(z) with z^N/z^N
    N = max(len(np), len(dp)) - 1
    num = Add(*[ T**(N-i) * c * (z-1)**i * (alpha * z + 1 - alpha)**(N-i) for c, i in zip(np[::-1], range(len(np))) ])
    den = Add(*[ T**(N-i) * c * (z-1)**i * (alpha * z + 1 - alpha)**(N-i) for c, i in zip(dp[::-1], range(len(dp))) ])

    num_coefs = num.as_poly(z).all_coeffs()
    den_coefs = den.as_poly(z).all_coeffs()

    para = den_coefs[0]
    num_coefs = [coef/para for coef in num_coefs]
    den_coefs = [coef/para for coef in den_coefs]

    return num_coefs, den_coefs

