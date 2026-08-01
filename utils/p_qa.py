
def PQa(P_0, Q_0, D):
    r"""
    Returns useful information needed to solve the Pell equation.

    Explanation
    ===========

    There are six sequences of integers defined related to the continued
    fraction representation of `\\frac{P + \sqrt{D}}{Q}`, namely {`P_{i}`},
    {`Q_{i}`}, {`a_{i}`},{`A_{i}`}, {`B_{i}`}, {`G_{i}`}. ``PQa()`` Returns
    these values as a 6-tuple in the same order as mentioned above. Refer [1]_
    for more detailed information.

    Usage
    =====

    ``PQa(P_0, Q_0, D)``: ``P_0``, ``Q_0`` and ``D`` are integers corresponding
    to `P_{0}`, `Q_{0}` and `D` in the continued fraction
    `\\frac{P_{0} + \sqrt{D}}{Q_{0}}`.
    Also it's assumed that `P_{0}^2 == D mod(|Q_{0}|)` and `D` is square free.

    Examples
    ========

    >>> from sympy.solvers.diophantine.diophantine import PQa
    >>> pqa = PQa(13, 4, 5) # (13 + sqrt(5))/4
    >>> next(pqa) # (P_0, Q_0, a_0, A_0, B_0, G_0)
    (13, 4, 3, 3, 1, -1)
    >>> next(pqa) # (P_1, Q_1, a_1, A_1, B_1, G_1)
    (-1, 1, 1, 4, 1, 3)

    References
    ==========

    .. [1] Solving the generalized Pell equation x^2 - Dy^2 = N, John P.
        Robertson, July 31, 2004, Pages 4 - 8. https://web.archive.org/web/20160323033128/http://www.jpr2718.org/pell.pdf
    """
    sqD = isqrt(D)
    A2 = B1 = 0
    A1 = B2 = 1
    G1 = Q_0
    G2 = -P_0
    P_i = P_0
    Q_i = Q_0

    while True:
        a_i = (P_i + sqD) // Q_i
        A1, A2 = a_i*A1 + A2, A1
        B1, B2 = a_i*B1 + B2, B1
        G1, G2 = a_i*G1 + G2, G1
        yield P_i, Q_i, a_i, A1, B1, G1

        P_i = a_i*Q_i - P_i
        Q_i = (D - P_i**2) // Q_i

