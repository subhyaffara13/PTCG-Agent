
def StudentT(name, nu):
    r"""
    Create a continuous random variable with a student's t distribution.

    Explanation
    ===========

    The density of the student's t distribution is given by

    .. math::
        f(x) := \frac{\Gamma \left(\frac{\nu+1}{2} \right)}
                {\sqrt{\nu\pi}\Gamma \left(\frac{\nu}{2} \right)}
                \left(1+\frac{x^2}{\nu} \right)^{-\frac{\nu+1}{2}}

    Parameters
    ==========

    nu : Real number, `\nu > 0`, the degrees of freedom

    Returns
    =======

    RandomSymbol

    Examples
    ========

    >>> from sympy.stats import StudentT, density, cdf
    >>> from sympy import Symbol, pprint

    >>> nu = Symbol("nu", positive=True)
    >>> z = Symbol("z")

    >>> X = StudentT("x", nu)

    >>> D = density(X)(z)
    >>> pprint(D, use_unicode=False)
               nu   1
             - -- - -
               2    2
     /     2\
     |    z |
     |1 + --|
     \    nu/
    -----------------
      ____  /     nu\
    \/ nu *B|1/2, --|
            \     2 /

    >>> cdf(X)(z)
    1/2 + z*gamma(nu/2 + 1/2)*hyper((1/2, nu/2 + 1/2), (3/2,),
                                -z**2/nu)/(sqrt(pi)*sqrt(nu)*gamma(nu/2))


    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Student_t-distribution
    .. [2] https://mathworld.wolfram.com/Studentst-Distribution.html

    """

    return rv(name, StudentTDistribution, (nu, ))

