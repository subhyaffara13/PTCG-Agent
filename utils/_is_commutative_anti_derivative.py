
def _is_commutative_anti_derivative(A, t):
    r"""
    Helper function for determining if the Matrix passed is commutative with its antiderivative

    Explanation
    ===========

    This function checks if the Matrix $A$ passed is commutative with its antiderivative with respect
    to the independent variable $t$.

    .. math::
        B(t) = \int A(t) dt

    The function outputs two values, first one being the antiderivative $B(t)$, second one being a
    boolean value, if True, then the matrix $A(t)$ passed is commutative with $B(t)$, else the matrix
    passed isn't commutative with $B(t)$.

    Parameters
    ==========

    A : Matrix
        The matrix which has to be checked
    t : Symbol
        Independent variable

    Examples
    ========

    >>> from sympy import symbols, Matrix
    >>> from sympy.solvers.ode.systems import _is_commutative_anti_derivative
    >>> t = symbols("t")
    >>> A = Matrix([[1, t], [-t, 1]])

    >>> B, is_commuting = _is_commutative_anti_derivative(A, t)
    >>> is_commuting
    True

    Returns
    =======

    Matrix, Boolean

    """
    B = integrate(A, t)
    is_commuting = (B*A - A*B).applyfunc(expand).applyfunc(factor_terms).is_zero_matrix

    is_commuting = False if is_commuting is None else is_commuting

    return B, is_commuting

