
def trigsimp_groebner(expr, hints=[], quick=False, order="grlex",
                      polynomial=False):
    """
    Simplify trigonometric expressions using a groebner basis algorithm.

    Explanation
    ===========

    This routine takes a fraction involving trigonometric or hyperbolic
    expressions, and tries to simplify it. The primary metric is the
    total degree. Some attempts are made to choose the simplest possible
    expression of the minimal degree, but this is non-rigorous, and also
    very slow (see the ``quick=True`` option).

    If ``polynomial`` is set to True, instead of simplifying numerator and
    denominator together, this function just brings numerator and denominator
    into a canonical form. This is much faster, but has potentially worse
    results. However, if the input is a polynomial, then the result is
    guaranteed to be an equivalent polynomial of minimal degree.

    The most important option is hints. Its entries can be any of the
    following:

    - a natural number
    - a function
    - an iterable of the form (func, var1, var2, ...)
    - anything else, interpreted as a generator

    A number is used to indicate that the search space should be increased.
    A function is used to indicate that said function is likely to occur in a
    simplified expression.
    An iterable is used indicate that func(var1 + var2 + ...) is likely to
    occur in a simplified .
    An additional generator also indicates that it is likely to occur.
    (See examples below).

    This routine carries out various computationally intensive algorithms.
    The option ``quick=True`` can be used to suppress one particularly slow
    step (at the expense of potentially more complicated results, but never at
    the expense of increased total degree).

    Examples
    ========

    >>> from sympy.abc import x, y
    >>> from sympy import sin, tan, cos, sinh, cosh, tanh
    >>> from sympy.simplify.trigsimp import trigsimp_groebner

    Suppose you want to simplify ``sin(x)*cos(x)``. Naively, nothing happens:

    >>> ex = sin(x)*cos(x)
    >>> trigsimp_groebner(ex)
    sin(x)*cos(x)

    This is because ``trigsimp_groebner`` only looks for a simplification
    involving just ``sin(x)`` and ``cos(x)``. You can tell it to also try
    ``2*x`` by passing ``hints=[2]``:

    >>> trigsimp_groebner(ex, hints=[2])
    sin(2*x)/2
    >>> trigsimp_groebner(sin(x)**2 - cos(x)**2, hints=[2])
    -cos(2*x)

    Increasing the search space this way can quickly become expensive. A much
    faster way is to give a specific expression that is likely to occur:

    >>> trigsimp_groebner(ex, hints=[sin(2*x)])
    sin(2*x)/2

    Hyperbolic expressions are similarly supported:

    >>> trigsimp_groebner(sinh(2*x)/sinh(x))
    2*cosh(x)

    Note how no hints had to be passed, since the expression already involved
    ``2*x``.

    The tangent function is also supported. You can either pass ``tan`` in the
    hints, to indicate that tan should be tried whenever cosine or sine are,
    or you can pass a specific generator:

    >>> trigsimp_groebner(sin(x)/cos(x), hints=[tan])
    tan(x)
    >>> trigsimp_groebner(sinh(x)/cosh(x), hints=[tanh(x)])
    tanh(x)

    Finally, you can use the iterable form to suggest that angle sum formulae
    should be tried:

    >>> ex = (tan(x) + tan(y))/(1 - tan(x)*tan(y))
    >>> trigsimp_groebner(ex, hints=[(tan, x, y)])
    tan(x + y)
    """
    # TODO
    #  - preprocess by replacing everything by funcs we can handle
    # - optionally use cot instead of tan
    # - more intelligent hinting.
    #     For example, if the ideal is small, and we have sin(x), sin(y),
    #     add sin(x + y) automatically... ?
    # - algebraic numbers ...
    # - expressions of lowest degree are not distinguished properly
    #   e.g. 1 - sin(x)**2
    # - we could try to order the generators intelligently, so as to influence
    #   which monomials appear in the quotient basis

    # THEORY
    # ------
    # Ratsimpmodprime above can be used to "simplify" a rational function
    # modulo a prime ideal. "Simplify" mainly means finding an equivalent
    # expression of lower total degree.
    #
    # We intend to use this to simplify trigonometric functions. To do that,
    # we need to decide (a) which ring to use, and (b) modulo which ideal to
    # simplify. In practice, (a) means settling on a list of "generators"
    # a, b, c, ..., such that the fraction we want to simplify is a rational
    # function in a, b, c, ..., with coefficients in ZZ (integers).
    # (2) means that we have to decide what relations to impose on the
    # generators. There are two practical problems:
    #   (1) The ideal has to be *prime* (a technical term).
    #   (2) The relations have to be polynomials in the generators.
    #
    # We typically have two kinds of generators:
    # - trigonometric expressions, like sin(x), cos(5*x), etc
    # - "everything else", like gamma(x), pi, etc.
    #
    # Since this function is trigsimp, we will concentrate on what to do with
    # trigonometric expressions. We can also simplify hyperbolic expressions,
    # but the extensions should be clear.
    #
    # One crucial point is that all *other* generators really should behave
    # like indeterminates. In particular if (say) "I" is one of them, then
    # in fact I**2 + 1 = 0 and we may and will compute non-sensical
    # expressions. However, we can work with a dummy and add the relation
    # I**2 + 1 = 0 to our ideal, then substitute back in the end.
    #
    # Now regarding trigonometric generators. We split them into groups,
    # according to the argument of the trigonometric functions. We want to
    # organise this in such a way that most trigonometric identities apply in
    # the same group. For example, given sin(x), cos(2*x) and cos(y), we would
    # group as [sin(x), cos(2*x)] and [cos(y)].
    #
    # Our prime ideal will be built in three steps:
    # (1) For each group, compute a "geometrically prime" ideal of relations.
    #     Geometrically prime means that it generates a prime ideal in
    #     CC[gens], not just ZZ[gens].
    # (2) Take the union of all the generators of the ideals for all groups.
    #     By the geometric primality condition, this is still prime.
    # (3) Add further inter-group relations which preserve primality.
    #
    # Step (1) works as follows. We will isolate common factors in the
    # argument, so that all our generators are of the form sin(n*x), cos(n*x)
    # or tan(n*x), with n an integer. Suppose first there are no tan terms.
    # The ideal [sin(x)**2 + cos(x)**2 - 1] is geometrically prime, since
    # X**2 + Y**2 - 1 is irreducible over CC.
    # Now, if we have a generator sin(n*x), than we can, using trig identities,
    # express sin(n*x) as a polynomial in sin(x) and cos(x). We can add this
    # relation to the ideal, preserving geometric primality, since the quotient
    # ring is unchanged.
    # Thus we have treated all sin and cos terms.
    # For tan(n*x), we add a relation tan(n*x)*cos(n*x) - sin(n*x) = 0.
    # (This requires of course that we already have relations for cos(n*x) and
    # sin(n*x).) It is not obvious, but it seems that this preserves geometric
    # primality.
    # XXX A real proof would be nice. HELP!
    #     Sketch that <S**2 + C**2 - 1, C*T - S> is a prime ideal of
    #     CC[S, C, T]:
    #     - it suffices to show that the projective closure in CP**3 is
    #       irreducible
    #     - using the half-angle substitutions, we can express sin(x), tan(x),
    #       cos(x) as rational functions in tan(x/2)
    #     - from this, we get a rational map from CP**1 to our curve
    #     - this is a morphism, hence the curve is prime
    #
    # Step (2) is trivial.
    #
    # Step (3) works by adding selected relations of the form
    # sin(x + y) - sin(x)*cos(y) - sin(y)*cos(x), etc. Geometric primality is
    # preserved by the same argument as before.

    def parse_hints(hints):
        """Split hints into (n, funcs, iterables, gens)."""
        n = 1
        funcs, iterables, gens = [], [], []
        for e in hints:
            if isinstance(e, (SYMPY_INTS, Integer)):
                n = e
            elif isinstance(e, FunctionClass):
                funcs.append(e)
            elif iterable(e):
                iterables.append((e[0], e[1:]))
                # XXX sin(x+2y)?
                # Note: we go through polys so e.g.
                # sin(-x) -> -sin(x) -> sin(x)
                gens.extend(parallel_poly_from_expr(
                    [e[0](x) for x in e[1:]] + [e[0](Add(*e[1:]))])[1].gens)
            else:
                gens.append(e)
        return n, funcs, iterables, gens

    def build_ideal(x, terms):
        """
        Build generators for our ideal. ``Terms`` is an iterable with elements of
        the form (fn, coeff), indicating that we have a generator fn(coeff*x).

        If any of the terms is trigonometric, sin(x) and cos(x) are guaranteed
        to appear in terms. Similarly for hyperbolic functions. For tan(n*x),
        sin(n*x) and cos(n*x) are guaranteed.
        """
        I = []
        y = Dummy('y')
        for fn, coeff in terms:
            for c, s, t, rel in (
                    [cos, sin, tan, cos(x)**2 + sin(x)**2 - 1],
                    [cosh, sinh, tanh, cosh(x)**2 - sinh(x)**2 - 1]):
                if coeff == 1 and fn in [c, s]:
                    I.append(rel)
                elif fn == t:
                    I.append(t(coeff*x)*c(coeff*x) - s(coeff*x))
                elif fn in [c, s]:
                    cn = fn(coeff*y).expand(trig=True).subs(y, x)
                    I.append(fn(coeff*x) - cn)
        return list(set(I))

    def analyse_gens(gens, hints):
        """
        Analyse the generators ``gens``, using the hints ``hints``.

        The meaning of ``hints`` is described in the main docstring.
        Return a new list of generators, and also the ideal we should
        work with.
        """
        # First parse the hints
        n, funcs, iterables, extragens = parse_hints(hints)
        debug('n=%s   funcs: %s   iterables: %s    extragens: %s',
              (funcs, iterables, extragens))

        # We just add the extragens to gens and analyse them as before
        gens = list(gens)
        gens.extend(extragens)

        # remove duplicates
        funcs = list(set(funcs))
        iterables = list(set(iterables))
        gens = list(set(gens))

        # all the functions we can do anything with
        allfuncs = {sin, cos, tan, sinh, cosh, tanh}
        # sin(3*x) -> ((3, x), sin)
        trigterms = [(g.args[0].as_coeff_mul(), g.func) for g in gens
                     if g.func in allfuncs]
        # Our list of new generators - start with anything that we cannot
        # work with (i.e. is not a trigonometric term)
        freegens = [g for g in gens if g.func not in allfuncs]
        newgens = []
        trigdict = {}
        for (coeff, var), fn in trigterms:
            trigdict.setdefault(var, []).append((coeff, fn))
        res = [] # the ideal

        for key, val in trigdict.items():
            # We have now assembeled a dictionary. Its keys are common
            # arguments in trigonometric expressions, and values are lists of
            # pairs (fn, coeff). x0, (fn, coeff) in trigdict means that we
            # need to deal with fn(coeff*x0). We take the rational gcd of the
            # coeffs, call it ``gcd``. We then use x = x0/gcd as "base symbol",
            # all other arguments are integral multiples thereof.
            # We will build an ideal which works with sin(x), cos(x).
            # If hint tan is provided, also work with tan(x). Moreover, if
            # n > 1, also work with sin(k*x) for k <= n, and similarly for cos
            # (and tan if the hint is provided). Finally, any generators which
            # the ideal does not work with but we need to accommodate (either
            # because it was in expr or because it was provided as a hint)
            # we also build into the ideal.
            # This selection process is expressed in the list ``terms``.
            # build_ideal then generates the actual relations in our ideal,
            # from this list.
            fns = [x[1] for x in val]
            val = [x[0] for x in val]
            gcd = reduce(igcd, val)
            terms = [(fn, v/gcd) for (fn, v) in zip(fns, val)]
            fs = set(funcs + fns)
            for c, s, t in ([cos, sin, tan], [cosh, sinh, tanh]):
                if any(x in fs for x in (c, s, t)):
                    fs.add(c)
                    fs.add(s)
            for fn in fs:
                terms.extend((fn, k) for k in range(1, n + 1))
            extra = []
            for fn, v in terms:
                if fn == tan:
                    extra.append((sin, v))
                    extra.append((cos, v))
                if fn in [sin, cos] and tan in fs:
                    extra.append((tan, v))
                if fn == tanh:
                    extra.append((sinh, v))
                    extra.append((cosh, v))
                if fn in [sinh, cosh] and tanh in fs:
                    extra.append((tanh, v))
            terms.extend(extra)
            x = gcd*Mul(*key)
            r = build_ideal(x, terms)
            res.extend(r)
            newgens.extend({fn(v*x) for fn, v in terms})

        # Add generators for compound expressions from iterables
        for fn, args in iterables:
            if fn == tan:
                # Tan expressions are recovered from sin and cos.
                iterables.extend([(sin, args), (cos, args)])
            elif fn == tanh:
                # Tanh expressions are recovered from sihn and cosh.
                iterables.extend([(sinh, args), (cosh, args)])
            else:
                dummys = symbols('d:%i' % len(args), cls=Dummy)
                expr = fn( Add(*dummys)).expand(trig=True).subs(list(zip(dummys, args)))
                res.append(fn(Add(*args)) - expr)

        if myI in gens:
            res.append(myI**2 + 1)
            freegens.remove(myI)
            newgens.append(myI)

        return res, freegens, newgens

    myI = Dummy('I')
    expr = expr.subs(S.ImaginaryUnit, myI)
    subs = [(myI, S.ImaginaryUnit)]

    num, denom = cancel(expr).as_numer_denom()
    try:
        (pnum, pdenom), opt = parallel_poly_from_expr([num, denom])
    except PolificationFailed:
        return expr
    debug('initial gens:', opt.gens)
    ideal, freegens, gens = analyse_gens(opt.gens, hints)
    debug('ideal:', ideal)
    debug('new gens:', gens, " -- len", len(gens))
    debug('free gens:', freegens, " -- len", len(gens))
    # NOTE we force the domain to be ZZ to stop polys from injecting generators
    #      (which is usually a sign of a bug in the way we build the ideal)
    if not gens:
        return expr
    G = groebner(ideal, order=order, gens=gens, domain=ZZ)
    debug('groebner basis:', list(G), " -- len", len(G))

    # If our fraction is a polynomial in the free generators, simplify all
    # coefficients separately:

    from sympy.simplify.ratsimp import ratsimpmodprime

    if freegens and pdenom.has_only_gens(*set(gens).intersection(pdenom.gens)):
        num = Poly(num, gens=gens+freegens).eject(*gens)
        res = []
        for monom, coeff in num.terms():
            ourgens = set(parallel_poly_from_expr([coeff, denom])[1].gens)
            # We compute the transitive closure of all generators that can
            # be reached from our generators through relations in the ideal.
            changed = True
            while changed:
                changed = False
                for p in ideal:
                    p = Poly(p)
                    if not ourgens.issuperset(p.gens) and \
                       not p.has_only_gens(*set(p.gens).difference(ourgens)):
                        changed = True
                        ourgens.update(p.exclude().gens)
            # NOTE preserve order!
            realgens = [x for x in gens if x in ourgens]
            # The generators of the ideal have now been (implicitly) split
            # into two groups: those involving ourgens and those that don't.
            # Since we took the transitive closure above, these two groups
            # live in subgrings generated by a *disjoint* set of variables.
            # Any sensible groebner basis algorithm will preserve this disjoint
            # structure (i.e. the elements of the groebner basis can be split
            # similarly), and and the two subsets of the groebner basis then
            # form groebner bases by themselves. (For the smaller generating
            # sets, of course.)
            ourG = [g.as_expr() for g in G.polys if
                    g.has_only_gens(*ourgens.intersection(g.gens))]
            res.append(Mul(*[a**b for a, b in zip(freegens, monom)]) * \
                       ratsimpmodprime(coeff/denom, ourG, order=order,
                                       gens=realgens, quick=quick, domain=ZZ,
                                       polynomial=polynomial).subs(subs))
        return Add(*res)
        # NOTE The following is simpler and has less assumptions on the
        #      groebner basis algorithm. If the above turns out to be broken,
        #      use this.
        return Add(*[Mul(*[a**b for a, b in zip(freegens, monom)]) * \
                     ratsimpmodprime(coeff/denom, list(G), order=order,
                                     gens=gens, quick=quick, domain=ZZ)
                     for monom, coeff in num.terms()])
    else:
        return ratsimpmodprime(
            expr, list(G), order=order, gens=freegens+gens,
            quick=quick, domain=ZZ, polynomial=polynomial).subs(subs)

