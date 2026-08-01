
def _galois_group_degree_4_root_approx(T, max_tries=30, randomize=False):
    r"""
    Compute the Galois group of a polynomial of degree 4.

    Explanation
    ===========

    Follows Alg 6.3.7 of [1], using a pure root approximation approach.

    """
    from sympy.combinatorics.permutations import Permutation
    from sympy.combinatorics.galois import S4TransitiveSubgroups

    X = symbols('X0 X1 X2 X3')
    # We start by considering the resolvent for the form
    #   F = X0*X2 + X1*X3
    # and the group G = S4. In this case, the stabilizer H is D4 = < (0123), (02) >,
    # and a set of representatives of G/H is {I, (01), (03)}
    F1 = X[0]*X[2] + X[1]*X[3]
    s1 = [
        Permutation(3),
        Permutation(3)(0, 1),
        Permutation(3)(0, 3)
    ]
    R1 = Resolvent(F1, X, s1)

    # In the second half of the algorithm (if we reach it), we use another
    # form and set of coset representatives. However, we may need to permute
    # them first, so cannot form their resolvent now.
    F2_pre = X[0]*X[1]**2 + X[1]*X[2]**2 + X[2]*X[3]**2 + X[3]*X[0]**2
    s2_pre = [
        Permutation(3),
        Permutation(3)(0, 2)
    ]

    history = set()
    for i in range(max_tries):
        if i > 0:
            # If we're retrying, need a new polynomial T.
            _, T = tschirnhausen_transformation(T, max_tries=max_tries,
                                                history=history,
                                                fixed_order=not randomize)

        R_dup, _, i0 = R1.eval_for_poly(T, find_integer_root=True)
        # If R is not squarefree, must retry.
        if not dup_sqf_p(R_dup, ZZ):
            continue

        # By Prop 6.3.1 of [1], Gal(T) is contained in A4 iff disc(T) is square.
        sq_disc = has_square_disc(T)

        if i0 is None:
            # By Thm 6.3.3 of [1], Gal(T) is not conjugate to any subgroup of the
            # stabilizer H = D4 that we chose. This means Gal(T) is either A4 or S4.
            return ((S4TransitiveSubgroups.A4, True) if sq_disc
                    else (S4TransitiveSubgroups.S4, False))

        # Gal(T) is conjugate to a subgroup of H = D4, so it is either V, C4
        # or D4 itself.

        if sq_disc:
            # Neither C4 nor D4 is contained in A4, so Gal(T) must be V.
            return (S4TransitiveSubgroups.V, True)

        # Gal(T) can only be D4 or C4.
        # We will now use our second resolvent, with G being that conjugate of D4 that
        # Gal(T) is contained in. To determine the right conjugate, we will need
        # the permutation corresponding to the integer root we found.
        sigma = s1[i0]
        # Applying sigma means permuting the args of F, and
        # conjugating the set of coset representatives.
        F2 = F2_pre.subs(zip(X, sigma(X)), simultaneous=True)
        s2 = [sigma*tau*sigma for tau in s2_pre]
        R2 = Resolvent(F2, X, s2)
        R_dup, _, _ = R2.eval_for_poly(T)
        d = dup_discriminant(R_dup, ZZ)
        # If d is zero (R has a repeated root), must retry.
        if d == 0:
            continue
        if is_square(d):
            return (S4TransitiveSubgroups.C4, False)
        else:
            return (S4TransitiveSubgroups.D4, False)

    raise MaxTriesException

