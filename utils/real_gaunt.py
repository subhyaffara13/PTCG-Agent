
def real_gaunt(l_1, l_2, l_3, mu_1, mu_2, mu_3, prec=None):
    r"""
    Calculate the real Gaunt coefficient.

    Explanation
    ===========

    The real Gaunt coefficient is defined as the integral over three
    real spherical harmonics:

    .. math::
        \begin{aligned}
        \operatorname{RealGaunt}(l_1,l_2,l_3,\mu_1,\mu_2,\mu_3)
        &=\int Z^{\mu_1}_{l_1}(\Omega)
         Z^{\mu_2}_{l_2}(\Omega) Z^{\mu_3}_{l_3}(\Omega) \,d\Omega \\
        \end{aligned}

    Alternatively, it can be defined in terms of the standard Gaunt
    coefficient by relating the real spherical harmonics to the standard
    spherical harmonics via a unitary transformation `U`, i.e.
    `Z^{\mu}_{l}(\Omega)=\sum_{m'}U^{\mu}_{m'}Y^{m'}_{l}(\Omega)` [Homeier96]_.
    The real Gaunt coefficient is then defined as

    .. math::
        \begin{aligned}
        \operatorname{RealGaunt}(l_1,l_2,l_3,\mu_1,\mu_2,\mu_3)
        &=\int Z^{\mu_1}_{l_1}(\Omega)
         Z^{\mu_2}_{l_2}(\Omega) Z^{\mu_3}_{l_3}(\Omega) \,d\Omega \\
        &=\sum_{m'_1 m'_2 m'_3} U^{\mu_1}_{m'_1}U^{\mu_2}_{m'_2}U^{\mu_3}_{m'_3}
         \operatorname{Gaunt}(l_1,l_2,l_3,m'_1,m'_2,m'_3)
        \end{aligned}

    The unitary matrix `U` has components

    .. math::
        \begin{aligned}
        U^\mu_{m} = \delta_{|\mu||m|}*(\delta_{m0}\delta_{\mu 0} + \frac{1}{\sqrt{2}}\big[\Theta(\mu)\big(\delta_{m\mu}+(-1)^{m}\delta_{m-\mu}\big)
        +i \Theta(-\mu)\big((-1)^{m}\delta_{m\mu}-\delta_{m-\mu}\big)\big])
        \end{aligned}


    where `\delta_{ij}` is the Kronecker delta symbol and `\Theta` is a step
    function defined as

    .. math::
        \begin{aligned}
        \Theta(x) = \begin{cases} 1 \,\text{for}\, x > 0 \\ 0 \,\text{for}\, x \leq 0 \end{cases}
        \end{aligned}

    Parameters
    ==========

    l_1, l_2, l_3, mu_1, mu_2, mu_3 :
        Integer degree and order

    prec - precision, default: ``None``.
        Providing a precision can
        drastically speed up the calculation.

    Returns
    =======

    Rational number times the square root of a rational number.

    Examples
    ========
    >>> from sympy.physics.wigner import real_gaunt
    >>> real_gaunt(1,1,2,-1,1,-2)
    sqrt(15)/(10*sqrt(pi))
    >>> real_gaunt(10,10,20,-9,-9,0,prec=64)
    -0.00002480019791932209313156167176797577821140084216297395518482071448

    It is an error to use non-integer values for `l` and `\mu`::
        real_gaunt(2.8,0.5,1.3,0,0,0)
        Traceback (most recent call last):
        ...
        ValueError: l values must be integer

        real_gaunt(2,2,4,0.7,1,-3.4)
        Traceback (most recent call last):
        ...
        ValueError: mu values must be integer

    Notes
    =====

    The real Gaunt coefficient inherits from the standard Gaunt coefficient,
    the invariance under any permutation of the pairs `(l_i, \mu_i)` and the
    requirement that the sum of the `l_i` be even to yield a non-zero value.
    It also obeys the following symmetry rules:

    - zero for `l_1`, `l_2`, `l_3` not fulfilling the condition
      `l_1 \in \{l_{\text{max}}, l_{\text{max}}-2, \ldots, l_{\text{min}}\}`,
      where `l_{\text{max}} = l_2+l_3`,

      .. math::
          \begin{aligned}
          l_{\text{min}} = \begin{cases} \kappa(l_2, l_3, \mu_2, \mu_3) & \text{if}\,
          \kappa(l_2, l_3, \mu_2, \mu_3) + l_{\text{max}}\, \text{is even} \\
          \kappa(l_2, l_3, \mu_2, \mu_3)+1 & \text{if}\, \kappa(l_2, l_3, \mu_2, \mu_3) +
          l_{\text{max}}\, \text{is odd}\end{cases}
          \end{aligned}

      and `\kappa(l_2, l_3, \mu_2, \mu_3) = \max{\big(|l_2-l_3|, \min{\big(|\mu_2+\mu_3|,
      |\mu_2-\mu_3|\big)}\big)}`

    - zero for an odd number of negative `\mu_i`

    Algorithms
    ==========

    This function uses the algorithms of [Homeier96]_ and [Rasch03]_ to
    calculate the value of the real Gaunt coefficient exactly. Note that
    the formula used in [Rasch03]_ contains alternating sums over large
    factorials and is therefore unsuitable for finite precision arithmetic
    and only useful for a computer algebra system [Rasch03]_. However, this
    function can in principle use any algorithm that computes the Gaunt
    coefficient, so it is suitable for finite precision arithmetic in so far
    as the algorithm which computes the Gaunt coefficient is.
    """
    l_1, l_2, l_3, mu_1, mu_2, mu_3 = [
        as_int(i) for i in (l_1, l_2, l_3, mu_1, mu_2, mu_3)]

    # check for quick exits
    if sum(1 for i in (mu_1, mu_2, mu_3) if i < 0) % 2:
        return S.Zero  # odd number of negative m
    if (l_1 + l_2 + l_3) % 2:
        return S.Zero  # sum of l is odd
    lmax = l_2 + l_3
    lmin = max(abs(l_2 - l_3), min(abs(mu_2 + mu_3), abs(mu_2 - mu_3)))
    if (lmin + lmax) % 2:
        lmin += 1
    if lmin not in range(lmax, lmin - 2, -2):
        return S.Zero

    kron_del = lambda i, j: 1 if i == j else 0
    s = lambda e: -1 if e % 2 else 1  #  (-1)**e to give +/-1, avoiding float when e<0

    t = lambda x: 1 if x > 0 else 0
    A = lambda mu, m: t(-mu) * (s(m) * kron_del(m, mu) - kron_del(m, -mu))
    B = lambda mu, m: t(mu) * (kron_del(m, mu) + s(m) * kron_del(m, -mu))
    U = lambda mu, m: kron_del(abs(mu), abs(m)) * (kron_del(mu, 0) * kron_del(m, 0) + (B(mu, m) + I * A(mu, m))/sqrt(2))

    ugnt = 0
    for m1 in range(-l_1, l_1+1):
        U1 = U(mu_1, m1)
        for m2 in range(-l_2, l_2+1):
            U2 = U(mu_2, m2)
            U3 = U(mu_3,-m1-m2)
            ugnt = ugnt + re(U1*U2*U3)*gaunt(l_1, l_2, l_3, m1, m2, -m1 - m2, prec=prec)

    return ugnt

