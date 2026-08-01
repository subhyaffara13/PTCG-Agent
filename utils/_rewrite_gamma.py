
def _rewrite_gamma(f, s, a, b):
    """
    Try to rewrite the product f(s) as a product of gamma functions,
    so that the inverse Mellin transform of f can be expressed as a meijer
    G function.

    Explanation
    ===========

    Return (an, ap), (bm, bq), arg, exp, fac such that
    G((an, ap), (bm, bq), arg/z**exp)*fac is the inverse Mellin transform of f(s).

    Raises IntegralTransformError or MellinTransformStripError on failure.

    It is asserted that f has no poles in the fundamental strip designated by
    (a, b). One of a and b is allowed to be None. The fundamental strip is
    important, because it determines the inversion contour.

    This function can handle exponentials, linear factors, trigonometric
    functions.

    This is a helper function for inverse_mellin_transform that will not
    attempt any transformations on f.

    Examples
    ========

    >>> from sympy.integrals.transforms import _rewrite_gamma
    >>> from sympy.abc import s
    >>> from sympy import oo
    >>> _rewrite_gamma(s*(s+3)*(s-1), s, -oo, oo)
    (([], [-3, 0, 1]), ([-2, 1, 2], []), 1, 1, -1)
    >>> _rewrite_gamma((s-1)**2, s, -oo, oo)
    (([], [1, 1]), ([2, 2], []), 1, 1, 1)

    Importance of the fundamental strip:

    >>> _rewrite_gamma(1/s, s, 0, oo)
    (([1], []), ([], [0]), 1, 1, 1)
    >>> _rewrite_gamma(1/s, s, None, oo)
    (([1], []), ([], [0]), 1, 1, 1)
    >>> _rewrite_gamma(1/s, s, 0, None)
    (([1], []), ([], [0]), 1, 1, 1)
    >>> _rewrite_gamma(1/s, s, -oo, 0)
    (([], [1]), ([0], []), 1, 1, -1)
    >>> _rewrite_gamma(1/s, s, None, 0)
    (([], [1]), ([0], []), 1, 1, -1)
    >>> _rewrite_gamma(1/s, s, -oo, None)
    (([], [1]), ([0], []), 1, 1, -1)

    >>> _rewrite_gamma(2**(-s+3), s, -oo, oo)
    (([], []), ([], []), 1/2, 1, 8)
    """
    # Our strategy will be as follows:
    # 1) Guess a constant c such that the inversion integral should be
    #    performed wrt s'=c*s (instead of plain s). Write s for s'.
    # 2) Process all factors, rewrite them independently as gamma functions in
    #    argument s, or exponentials of s.
    # 3) Try to transform all gamma functions s.t. they have argument
    #    a+s or a-s.
    # 4) Check that the resulting G function parameters are valid.
    # 5) Combine all the exponentials.

    a_, b_ = S([a, b])

    def left(c, is_numer):
        """
        Decide whether pole at c lies to the left of the fundamental strip.
        """
        # heuristically, this is the best chance for us to solve the inequalities
        c = expand(re(c))
        if a_ is None and b_ is S.Infinity:
            return True
        if a_ is None:
            return c < b_
        if b_ is None:
            return c <= a_
        if (c >= b_) == True:
            return False
        if (c <= a_) == True:
            return True
        if is_numer:
            return None
        if a_.free_symbols or b_.free_symbols or c.free_symbols:
            return None  # XXX
            #raise IntegralTransformError('Inverse Mellin', f,
            #                     'Could not determine position of singularity %s'
            #                     ' relative to fundamental strip' % c)
        raise MellinTransformStripError('Pole inside critical strip?')

    # 1)
    s_multipliers = []
    for g in f.atoms(gamma):
        if not g.has(s):
            continue
        arg = g.args[0]
        if arg.is_Add:
            arg = arg.as_independent(s)[1]
        coeff, _ = arg.as_coeff_mul(s)
        s_multipliers += [coeff]
    for g in f.atoms(sin, cos, tan, cot):
        if not g.has(s):
            continue
        arg = g.args[0]
        if arg.is_Add:
            arg = arg.as_independent(s)[1]
        coeff, _ = arg.as_coeff_mul(s)
        s_multipliers += [coeff/pi]
    s_multipliers = [Abs(x) if x.is_extended_real else x for x in s_multipliers]
    common_coefficient = S.One
    for x in s_multipliers:
        if not x.is_Rational:
            common_coefficient = x
            break
    s_multipliers = [x/common_coefficient for x in s_multipliers]
    if not (all(x.is_Rational for x in s_multipliers) and
            common_coefficient.is_extended_real):
        raise IntegralTransformError("Gamma", None, "Nonrational multiplier")
    s_multiplier = common_coefficient/reduce(ilcm, [S(x.q)
                                             for x in s_multipliers], S.One)
    if s_multiplier == common_coefficient:
        if len(s_multipliers) == 0:
            s_multiplier = common_coefficient
        else:
            s_multiplier = common_coefficient \
                *reduce(igcd, [S(x.p) for x in s_multipliers])

    f = f.subs(s, s/s_multiplier)
    fac = S.One/s_multiplier
    exponent = S.One/s_multiplier
    if a_ is not None:
        a_ *= s_multiplier
    if b_ is not None:
        b_ *= s_multiplier

    # 2)
    numer, denom = f.as_numer_denom()
    numer = Mul.make_args(numer)
    denom = Mul.make_args(denom)
    args = list(zip(numer, repeat(True))) + list(zip(denom, repeat(False)))

    facs = []
    dfacs = []
    # *_gammas will contain pairs (a, c) representing Gamma(a*s + c)
    numer_gammas = []
    denom_gammas = []
    # exponentials will contain bases for exponentials of s
    exponentials = []

    def exception(fact):
        return IntegralTransformError("Inverse Mellin", f, "Unrecognised form '%s'." % fact)
    while args:
        fact, is_numer = args.pop()
        if is_numer:
            ugammas, lgammas = numer_gammas, denom_gammas
            ufacs = facs
        else:
            ugammas, lgammas = denom_gammas, numer_gammas
            ufacs = dfacs

        def linear_arg(arg):
            """ Test if arg is of form a*s+b, raise exception if not. """
            if not arg.is_polynomial(s):
                raise exception(fact)
            p = Poly(arg, s)
            if p.degree() != 1:
                raise exception(fact)
            return p.all_coeffs()

        # constants
        if not fact.has(s):
            ufacs += [fact]
        # exponentials
        elif fact.is_Pow or isinstance(fact, exp):
            if fact.is_Pow:
                base = fact.base
                exp_ = fact.exp
            else:
                base = exp_polar(1)
                exp_ = fact.exp
            if exp_.is_Integer:
                cond = is_numer
                if exp_ < 0:
                    cond = not cond
                args += [(base, cond)]*Abs(exp_)
                continue
            elif not base.has(s):
                a, b = linear_arg(exp_)
                if not is_numer:
                    base = 1/base
                exponentials += [base**a]
                facs += [base**b]
            else:
                raise exception(fact)
        # linear factors
        elif fact.is_polynomial(s):
            p = Poly(fact, s)
            if p.degree() != 1:
                # We completely factor the poly. For this we need the roots.
                # Now roots() only works in some cases (low degree), and CRootOf
                # only works without parameters. So try both...
                coeff = p.LT()[1]
                rs = roots(p, s)
                if len(rs) != p.degree():
                    rs = CRootOf.all_roots(p)
                ufacs += [coeff]
                args += [(s - c, is_numer) for c in rs]
                continue
            a, c = p.all_coeffs()
            ufacs += [a]
            c /= -a
            # Now need to convert s - c
            if left(c, is_numer):
                ugammas += [(S.One, -c + 1)]
                lgammas += [(S.One, -c)]
            else:
                ufacs += [-1]
                ugammas += [(S.NegativeOne, c + 1)]
                lgammas += [(S.NegativeOne, c)]
        elif isinstance(fact, gamma):
            a, b = linear_arg(fact.args[0])
            if is_numer:
                if (a > 0 and (left(-b/a, is_numer) == False)) or \
                   (a < 0 and (left(-b/a, is_numer) == True)):
                    raise NotImplementedError(
                        'Gammas partially over the strip.')
            ugammas += [(a, b)]
        elif isinstance(fact, sin):
            # We try to re-write all trigs as gammas. This is not in
            # general the best strategy, since sometimes this is impossible,
            # but rewriting as exponentials would work. However trig functions
            # in inverse mellin transforms usually all come from simplifying
            # gamma terms, so this should work.
            a = fact.args[0]
            if is_numer:
                # No problem with the poles.
                gamma1, gamma2, fac_ = gamma(a/pi), gamma(1 - a/pi), pi
            else:
                gamma1, gamma2, fac_ = _rewrite_sin(linear_arg(a), s, a_, b_)
            args += [(gamma1, not is_numer), (gamma2, not is_numer)]
            ufacs += [fac_]
        elif isinstance(fact, tan):
            a = fact.args[0]
            args += [(sin(a, evaluate=False), is_numer),
                     (sin(pi/2 - a, evaluate=False), not is_numer)]
        elif isinstance(fact, cos):
            a = fact.args[0]
            args += [(sin(pi/2 - a, evaluate=False), is_numer)]
        elif isinstance(fact, cot):
            a = fact.args[0]
            args += [(sin(pi/2 - a, evaluate=False), is_numer),
                     (sin(a, evaluate=False), not is_numer)]
        else:
            raise exception(fact)

    fac *= Mul(*facs)/Mul(*dfacs)

    # 3)
    an, ap, bm, bq = [], [], [], []
    for gammas, plus, minus, is_numer in [(numer_gammas, an, bm, True),
                                          (denom_gammas, bq, ap, False)]:
        while gammas:
            a, c = gammas.pop()
            if a != -1 and a != +1:
                # We use the gamma function multiplication theorem.
                p = Abs(S(a))
                newa = a/p
                newc = c/p
                if not a.is_Integer:
                    raise TypeError("a is not an integer")
                for k in range(p):
                    gammas += [(newa, newc + k/p)]
                if is_numer:
                    fac *= (2*pi)**((1 - p)/2) * p**(c - S.Half)
                    exponentials += [p**a]
                else:
                    fac /= (2*pi)**((1 - p)/2) * p**(c - S.Half)
                    exponentials += [p**(-a)]
                continue
            if a == +1:
                plus.append(1 - c)
            else:
                minus.append(c)

    # 4)
    # TODO

    # 5)
    arg = Mul(*exponentials)

    # for testability, sort the arguments
    an.sort(key=default_sort_key)
    ap.sort(key=default_sort_key)
    bm.sort(key=default_sort_key)
    bq.sort(key=default_sort_key)

    return (an, ap), (bm, bq), arg, exponent, fac

