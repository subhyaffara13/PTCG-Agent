
def clebsch_gordan(j_1, j_2, j_3, m_1, m_2, m_3):
    r"""
    Calculates the Clebsch-Gordan coefficient.
    `\left\langle j_1 m_1 \; j_2 m_2 | j_3 m_3 \right\rangle`.

    The reference for this function is [Edmonds74]_.

    Parameters
    ==========

    j_1, j_2, j_3, m_1, m_2, m_3 :
        Integer or half integer.

    Returns
    =======

    Rational number times the square root of a rational number.

    Examples
    ========

    >>> from sympy import S
    >>> from sympy.physics.wigner import clebsch_gordan
    >>> clebsch_gordan(S(3)/2, S(1)/2, 2, S(3)/2, S(1)/2, 2)
    1
    >>> clebsch_gordan(S(3)/2, S(1)/2, 1, S(3)/2, -S(1)/2, 1)
    sqrt(3)/2
    >>> clebsch_gordan(S(3)/2, S(1)/2, 1, -S(1)/2, S(1)/2, 0)
    -sqrt(2)/2

    Notes
    =====

    The Clebsch-Gordan coefficient will be evaluated via its relation
    to Wigner 3j symbols:

    .. math::

        \left\langle j_1 m_1 \; j_2 m_2 | j_3 m_3 \right\rangle
        =(-1)^{j_1-j_2+m_3} \sqrt{2j_3+1}
        \operatorname{Wigner3j}(j_1,j_2,j_3,m_1,m_2,-m_3)

    See also the documentation on Wigner 3j symbols which exhibit much
    higher symmetry relations than the Clebsch-Gordan coefficient.

    Authors
    =======

    - Jens Rasch (2009-03-24): initial version
    """
    j_1 = sympify(j_1)
    j_2 = sympify(j_2)
    j_3 = sympify(j_3)
    m_1 = sympify(m_1)
    m_2 = sympify(m_2)
    m_3 = sympify(m_3)

    w = wigner_3j(j_1, j_2, j_3, m_1, m_2, -m_3)

    return (-1) ** (j_1 - j_2 + m_3) * sqrt(2 * j_3 + 1) * w

