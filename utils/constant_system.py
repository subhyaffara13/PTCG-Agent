
def constant_system(A, u, DE):
    """
    Generate a system for the constant solutions.

    Explanation
    ===========

    Given a differential field (K, D) with constant field C = Const(K), a Matrix
    A, and a vector (Matrix) u with coefficients in K, returns the tuple
    (B, v, s), where B is a Matrix with coefficients in C and v is a vector
    (Matrix) such that either v has coefficients in C, in which case s is True
    and the solutions in C of Ax == u are exactly all the solutions of Bx == v,
    or v has a non-constant coefficient, in which case s is False Ax == u has no
    constant solution.

    This algorithm is used both in solving parametric problems and in
    determining if an element a of K is a derivative of an element of K or the
    logarithmic derivative of a K-radical using the structure theorem approach.

    Because Poly does not play well with Matrix yet, this algorithm assumes that
    all matrix entries are Basic expressions.
    """
    if not A:
        return A, u
    Au = A.row_join(u)
    Au, _ = Au.rref()
    # Warning: This will NOT return correct results if cancel() cannot reduce
    # an identically zero expression to 0.  The danger is that we might
    # incorrectly prove that an integral is nonelementary (such as
    # risch_integrate(exp((sin(x)**2 + cos(x)**2 - 1)*x**2), x).
    # But this is a limitation in computer algebra in general, and implicit
    # in the correctness of the Risch Algorithm is the computability of the
    # constant field (actually, this same correctness problem exists in any
    # algorithm that uses rref()).
    #
    # We therefore limit ourselves to constant fields that are computable
    # via the cancel() function, in order to prevent a speed bottleneck from
    # calling some more complex simplification function (rational function
    # coefficients will fall into this class).  Furthermore, (I believe) this
    # problem will only crop up if the integral explicitly contains an
    # expression in the constant field that is identically zero, but cannot
    # be reduced to such by cancel().  Therefore, a careful user can avoid this
    # problem entirely by being careful with the sorts of expressions that
    # appear in his integrand in the variables other than the integration
    # variable (the structure theorems should be able to completely decide these
    # problems in the integration variable).

    A, u = Au[:, :-1], Au[:, -1]

    D = lambda x: derivation(x, DE, basic=True)

    for j, i in itertools.product(range(A.cols), range(A.rows)):
        if A[i, j].expr.has(*DE.T):
            # This assumes that const(F(t0, ..., tn) == const(K) == F
            Ri = A[i, :]
            # Rm+1; m = A.rows
            DAij = D(A[i, j])
            Rm1 = Ri.applyfunc(lambda x: D(x) / DAij)
            um1 = D(u[i]) / DAij

            Aj = A[:, j]
            A = A - Aj * Rm1
            u = u - Aj * um1

            A = A.col_join(Rm1)
            u = u.col_join(Matrix([um1], u.gens))

    return (A, u)

