
def is_log_deriv_k_t_radical(fa, fd, DE, Df=True):
    r"""
    Checks if Df is the logarithmic derivative of a k(t)-radical.

    Explanation
    ===========

    b in k(t) can be written as the logarithmic derivative of a k(t) radical if
    there exist n in ZZ and u in k(t) with n, u != 0 such that n*b == Du/u.
    Either returns (ans, u, n, const) or None, which means that Df cannot be
    written as the logarithmic derivative of a k(t)-radical.  ans is a list of
    tuples such that Mul(*[i**j for i, j in ans]) == u.  This is useful for
    seeing exactly what elements of k(t) produce u.

    This function uses the structure theorem approach, which says that for any
    f in K, Df is the logarithmic derivative of a K-radical if and only if there
    are ri in QQ such that::

            ---               ---       Dt
            \    r  * Dt   +  \    r  *   i
            /     i     i     /     i   ---   =  Df.
            ---               ---        t
         i in L            i in E         i
               K/C(x)            K/C(x)


    Where C = Const(K), L_K/C(x) = { i in {1, ..., n} such that t_i is
    transcendental over C(x)(t_1, ..., t_i-1) and Dt_i = Da_i/a_i, for some a_i
    in C(x)(t_1, ..., t_i-1)* } (i.e., the set of all indices of logarithmic
    monomials of K over C(x)), and E_K/C(x) = { i in {1, ..., n} such that t_i
    is transcendental over C(x)(t_1, ..., t_i-1) and Dt_i/t_i = Da_i, for some
    a_i in C(x)(t_1, ..., t_i-1) } (i.e., the set of all indices of
    hyperexponential monomials of K over C(x)).  If K is an elementary extension
    over C(x), then the cardinality of L_K/C(x) U E_K/C(x) is exactly the
    transcendence degree of K over C(x).  Furthermore, because Const_D(K) ==
    Const_D(C(x)) == C, deg(Dt_i) == 1 when t_i is in E_K/C(x) and
    deg(Dt_i) == 0 when t_i is in L_K/C(x), implying in particular that E_K/C(x)
    and L_K/C(x) are disjoint.

    The sets L_K/C(x) and E_K/C(x) must, by their nature, be computed
    recursively using this same function.  Therefore, it is required to pass
    them as indices to D (or T).  L_args are the arguments of the logarithms
    indexed by L_K (i.e., if i is in L_K, then T[i] == log(L_args[i])).  This is
    needed to compute the final answer u such that n*f == Du/u.

    exp(f) will be the same as u up to a multiplicative constant.  This is
    because they will both behave the same as monomials.  For example, both
    exp(x) and exp(x + 1) == E*exp(x) satisfy Dt == t. Therefore, the term const
    is returned.  const is such that exp(const)*f == u.  This is calculated by
    subtracting the arguments of one exponential from the other.  Therefore, it
    is necessary to pass the arguments of the exponential terms in E_args.

    To handle the case where we are given Df, not f, use
    is_log_deriv_k_t_radical_in_field().

    See also
    ========

    is_log_deriv_k_t_radical_in_field, is_deriv_k

    """
    if Df:
        dfa, dfd = (fd*derivation(fa, DE) - fa*derivation(fd, DE)).cancel(fd**2,
            include=True)
    else:
        dfa, dfd = fa, fd

    # Our assumption here is that each monomial is recursively transcendental
    if len(DE.exts) != len(DE.D):
        if [i for i in DE.cases if i == 'tan'] or \
                ({i for i in DE.cases if i == 'primitive'} -
                        set(DE.indices('log'))):
            raise NotImplementedError("Real version of the structure "
                "theorems with hypertangent support is not yet implemented.")

        # TODO: What should really be done in this case?
        raise NotImplementedError("Nonelementary extensions not supported "
            "in the structure theorems.")

    E_part = [DE.D[i].quo(Poly(DE.T[i], DE.T[i])).as_expr() for i in DE.indices('exp')]
    L_part = [DE.D[i].as_expr() for i in DE.indices('log')]

    # The expression dfa/dfd might not be polynomial in any of its symbols so we
    # use a Dummy as the generator for PolyMatrix.
    dum = Dummy()
    lhs = Matrix([E_part + L_part], dum)
    rhs = Matrix([dfa.as_expr()/dfd.as_expr()], dum)

    A, u = constant_system(lhs, rhs, DE)

    u = u.to_Matrix()  # Poly to Expr

    if not A or not all(derivation(i, DE, basic=True).is_zero for i in u):
        # If the elements of u are not all constant
        # Note: See comment in constant_system

        # Also note: derivation(basic=True) calls cancel()
        return None
    else:
        if not all(i.is_Rational for i in u):
            # TODO: But maybe we can tell if they're not rational, like
            # log(2)/log(3). Also, there should be an option to continue
            # anyway, even if the result might potentially be wrong.
            raise NotImplementedError("Cannot work with non-rational "
                "coefficients in this case.")
        else:
            n = S.One*reduce(ilcm, [i.as_numer_denom()[1] for i in u])
            u *= n
            terms = ([DE.T[i] for i in DE.indices('exp')] +
                    [DE.extargs[i] for i in DE.indices('log')])
            ans = list(zip(terms, u))
            result = Mul(*[Pow(i, j) for i, j in ans])

            # exp(f) will be the same as result up to a multiplicative
            # constant.  We now find the log of that constant.
            argterms = ([DE.extargs[i] for i in DE.indices('exp')] +
                    [DE.T[i] for i in DE.indices('log')])
            const = cancel(fa.as_expr()/fd.as_expr() -
                Add(*[Mul(i, j/n) for i, j in zip(argterms, u)]))

            return (ans, result, n, const)

