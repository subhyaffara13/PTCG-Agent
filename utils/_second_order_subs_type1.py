
def _second_order_subs_type1(A, b, funcs, t):
    r"""
    For a linear, second order system of ODEs, a particular substitution.

    A system of the below form can be reduced to a linear first order system of
    ODEs:
    .. math::
        X'' = A(t) * (t*X' - X) + b(t)

    By substituting:
    .. math::  U = t*X' - X

    To get the system:
    .. math::  U' = t*(A(t)*U + b(t))

    Where $U$ is the vector of dependent variables, $X$ is the vector of dependent
    variables in `funcs` and $X'$ is the first order derivative of $X$ with respect to
    $t$. It may or may not reduce the system into linear first order system of ODEs.

    Then a check is made to determine if the system passed can be reduced or not, if
    this substitution works, then the system is reduced and its solved for the new
    substitution. After we get the solution for $U$:

    .. math::  U = a(t)

    We substitute and return the reduced system:

    .. math::
        a(t) = t*X' - X

    Parameters
    ==========

    A: Matrix
        Coefficient matrix($A(t)*t$) of the second order system of this form.
    b: Matrix
        Non-homogeneous term($b(t)$) of the system of ODEs.
    funcs: List
        List of dependent variables
    t: Symbol
        Independent variable of the system of ODEs.

    Returns
    =======

    List

    """

    U = Matrix([t*func.diff(t) - func for func in funcs])

    sol = linodesolve(A, t, t*b)
    reduced_eqs = [Eq(u, s) for s, u in zip(sol, U)]
    reduced_eqs = canonical_odes(reduced_eqs, funcs, t)[0]

    return reduced_eqs

