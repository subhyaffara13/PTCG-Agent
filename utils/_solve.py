
def _solve(M, rhs, method='GJ'):
    """Solves linear equation where the unique solution exists.

    Parameters
    ==========

    rhs : Matrix
        Vector representing the right hand side of the linear equation.

    method : string, optional
        If set to ``'GJ'`` or ``'GE'``, the Gauss-Jordan elimination will be
        used, which is implemented in the routine ``gauss_jordan_solve``.

        If set to ``'LU'``, ``LUsolve`` routine will be used.

        If set to ``'QR'``, ``QRsolve`` routine will be used.

        If set to ``'PINV'``, ``pinv_solve`` routine will be used.

        If set to ``'CRAMER'``, ``cramer_solve`` routine will be used.

        It also supports the methods available for special linear systems

        For positive definite systems:

        If set to ``'CH'``, ``cholesky_solve`` routine will be used.

        If set to ``'LDL'``, ``LDLsolve`` routine will be used.

        To use a different method and to compute the solution via the
        inverse, use a method defined in the .inv() docstring.

    Returns
    =======

    solutions : Matrix
        Vector representing the solution.

    Raises
    ======

    ValueError
        If there is not a unique solution then a ``ValueError`` will be
        raised.

        If ``M`` is not square, a ``ValueError`` and a different routine
        for solving the system will be suggested.
    """

    if method in ('GJ', 'GE'):
        try:
            soln, param = M.gauss_jordan_solve(rhs)

            if param:
                raise NonInvertibleMatrixError("Matrix det == 0; not invertible. "
                "Try ``M.gauss_jordan_solve(rhs)`` to obtain a parametric solution.")

        except ValueError:
            raise NonInvertibleMatrixError("Matrix det == 0; not invertible.")

        return soln

    elif method == 'LU':
        return M.LUsolve(rhs)
    elif method == 'CH':
        return M.cholesky_solve(rhs)
    elif method == 'QR':
        return M.QRsolve(rhs)
    elif method == 'LDL':
        return M.LDLsolve(rhs)
    elif method == 'PINV':
        return M.pinv_solve(rhs)
    elif method == 'CRAMER':
        return M.cramer_solve(rhs)
    else:
        return M.inv(method=method).multiply(rhs)


def _solve(f, *symbols, **flags):
    """Return a checked solution for *f* in terms of one or more of the
    symbols in the form of a list of dictionaries.

    If no method is implemented to solve the equation, a NotImplementedError
    will be raised. In the case that conversion of an expression to a Poly
    gives None a ValueError will be raised.
    """

    not_impl_msg = "No algorithms are implemented to solve equation %s"

    if len(symbols) != 1:
        # look for solutions for desired symbols that are independent
        # of symbols already solved for, e.g. if we solve for x = y
        # then no symbol having x in its solution will be returned.

        # First solve for linear symbols (since that is easier and limits
        # solution size) and then proceed with symbols appearing
        # in a non-linear fashion. Ideally, if one is solving a single
        # expression for several symbols, they would have to be
        # appear in factors of an expression, but we do not here
        # attempt factorization.  XXX perhaps handling a Mul
        # should come first in this routine whether there is
        # one or several symbols.
        nonlin_s = []
        got_s = set()
        rhs_s = set()
        result = []
        for s in symbols:
            xi, v = solve_linear(f, symbols=[s])
            if xi == s:
                # no need to check but we should simplify if desired
                if flags.get('simplify', True):
                    v = simplify(v)
                vfree = v.free_symbols
                if vfree & got_s:
                    # was linear, but has redundant relationship
                    # e.g. x - y = 0 has y == x is redundant for x == y
                    # so ignore
                    continue
                rhs_s |= vfree
                got_s.add(xi)
                result.append({xi: v})
            elif xi:  # there might be a non-linear solution if xi is not 0
                nonlin_s.append(s)
        if not nonlin_s:
            return result
        for s in nonlin_s:
            try:
                soln = _solve(f, s, **flags)
                for sol in soln:
                    if sol[s].free_symbols & got_s:
                        # depends on previously solved symbols: ignore
                        continue
                    got_s.add(s)
                    result.append(sol)
            except NotImplementedError:
                continue
        if got_s:
            return result
        else:
            raise NotImplementedError(not_impl_msg % f)

    # solve f for a single variable

    symbol = symbols[0]

    # expand binomials only if it has the unknown symbol
    f = f.replace(lambda e: isinstance(e, binomial) and e.has(symbol),
        lambda e: expand_func(e))

    # checking will be done unless it is turned off before making a
    # recursive call; the variables `checkdens` and `check` are
    # captured here (for reference below) in case flag value changes
    flags['check'] = checkdens = check = flags.pop('check', True)

    # build up solutions if f is a Mul
    if f.is_Mul:
        result = set()
        for m in f.args:
            if m in {S.NegativeInfinity, S.ComplexInfinity, S.Infinity}:
                result = set()
                break
            soln = _vsolve(m, symbol, **flags)
            result.update(set(soln))
        result = [{symbol: v} for v in result]
        if check:
            # all solutions have been checked but now we must
            # check that the solutions do not set denominators
            # in any factor to zero
            dens = flags.get('_denominators', _simple_dens(f, symbols))
            result = [s for s in result if
                not any(checksol(den, s, **flags) for den in
                        dens)]
        # set flags for quick exit at end; solutions for each
        # factor were already checked and simplified
        check = False
        flags['simplify'] = False

    elif f.is_Piecewise:
        result = set()
        if any(e.is_zero for e, c in f.args):
            f = f.simplify()  # failure imminent w/o help

        cond = neg = True
        for expr, cnd in f.args:
            # the explicit condition for this expr is the current cond
            # and none of the previous conditions
            cond = And(neg, cnd)
            neg = And(neg, ~cond)

            if expr.is_zero and cond.simplify() != False:
                raise NotImplementedError(filldedent('''
                    An expression is already zero when %s.
                    This means that in this *region* the solution
                    is zero but solve can only represent discrete,
                    not interval, solutions. If this is a spurious
                    interval it might be resolved with simplification
                    of the Piecewise conditions.''' % cond))
            candidates = _vsolve(expr, symbol, **flags)

            for candidate in candidates:
                if candidate in result:
                    # an unconditional value was already there
                    continue
                try:
                    v = cond.subs(symbol, candidate)
                    _eval_simplify = getattr(v, '_eval_simplify', None)
                    if _eval_simplify is not None:
                        # unconditionally take the simplification of v
                        v = _eval_simplify(ratio=2, measure=lambda x: 1)
                except TypeError:
                    # incompatible type with condition(s)
                    continue
                if v == False:
                    continue
                if v == True:
                    result.add(candidate)
                else:
                    result.add(Piecewise(
                        (candidate, v),
                        (S.NaN, True)))
        # solutions already checked and simplified
        # ****************************************
        return [{symbol: r} for r in result]
    else:
        # first see if it really depends on symbol and whether there
        # is only a linear solution
        f_num, sol = solve_linear(f, symbols=symbols)
        if f_num.is_zero or sol is S.NaN:
            return []
        elif f_num.is_Symbol:
            # no need to check but simplify if desired
            if flags.get('simplify', True):
                sol = simplify(sol)
            return [{f_num: sol}]

        poly = None
        # check for a single Add generator
        if not f_num.is_Add:
            add_args = [i for i in f_num.atoms(Add)
                if symbol in i.free_symbols]
            if len(add_args) == 1:
                gen = add_args[0]
                spart = gen.as_independent(symbol)[1].as_base_exp()[0]
                if spart == symbol:
                    try:
                        poly = Poly(f_num, spart)
                    except PolynomialError:
                        pass

        result = False  # no solution was obtained
        msg = ''  # there is no failure message

        # Poly is generally robust enough to convert anything to
        # a polynomial and tell us the different generators that it
        # contains, so we will inspect the generators identified by
        # polys to figure out what to do.

        # try to identify a single generator that will allow us to solve this
        # as a polynomial, followed (perhaps) by a change of variables if the
        # generator is not a symbol

        try:
            if poly is None:
                poly = Poly(f_num)
            if poly is None:
                raise ValueError('could not convert %s to Poly' % f_num)
        except GeneratorsNeeded:
            simplified_f = simplify(f_num)
            if simplified_f != f_num:
                return _solve(simplified_f, symbol, **flags)
            raise ValueError('expression appears to be a constant')

        gens = [g for g in poly.gens if g.has(symbol)]

        def _as_base_q(x):
            """Return (b**e, q) for x = b**(p*e/q) where p/q is the leading
            Rational of the exponent of x, e.g. exp(-2*x/3) -> (exp(x), 3)
            """
            b, e = x.as_base_exp()
            if e.is_Rational:
                return b, e.q
            if not e.is_Mul:
                return x, 1
            c, ee = e.as_coeff_Mul()
            if c.is_Rational and c is not S.One:  # c could be a Float
                return b**ee, c.q
            return x, 1

        if len(gens) > 1:
            # If there is more than one generator, it could be that the
            # generators have the same base but different powers, e.g.
            #   >>> Poly(exp(x) + 1/exp(x))
            #   Poly(exp(-x) + exp(x), exp(-x), exp(x), domain='ZZ')
            #
            # If unrad was not disabled then there should be no rational
            # exponents appearing as in
            #   >>> Poly(sqrt(x) + sqrt(sqrt(x)))
            #   Poly(sqrt(x) + x**(1/4), sqrt(x), x**(1/4), domain='ZZ')

            bases, qs = list(zip(*[_as_base_q(g) for g in gens]))
            bases = set(bases)

            if len(bases) > 1 or not all(q == 1 for q in qs):
                funcs = {b for b in bases if b.is_Function}

                trig = {_ for _ in funcs if
                    isinstance(_, TrigonometricFunction)}
                other = funcs - trig
                if not other and len(funcs.intersection(trig)) > 1:
                    newf = None
                    if f_num.is_Add and len(f_num.args) == 2:
                        # check for sin(x)**p = cos(x)**p
                        _args = f_num.args
                        t = a, b = [i.atoms(Function).intersection(
                            trig) for i in _args]
                        if all(len(i) == 1 for i in t):
                            a, b = [i.pop() for i in t]
                            if isinstance(a, cos):
                                a, b = b, a
                                _args = _args[::-1]
                            if isinstance(a, sin) and isinstance(b, cos
                                    ) and a.args[0] == b.args[0]:
                                # sin(x) + cos(x) = 0 -> tan(x) + 1 = 0
                                newf, _d = (TR2i(_args[0]/_args[1]) + 1
                                    ).as_numer_denom()
                                if not _d.is_Number:
                                    newf = None
                    if newf is None:
                        newf = TR1(f_num).rewrite(tan)
                    if newf != f_num:
                        # don't check the rewritten form --check
                        # solutions in the un-rewritten form below
                        flags['check'] = False
                        result = _solve(newf, symbol, **flags)
                        flags['check'] = check

                # just a simple case - see if replacement of single function
                # clears all symbol-dependent functions, e.g.
                # log(x) - log(log(x) - 1) - 3 can be solved even though it has
                # two generators.

                if result is False and funcs:
                    funcs = list(ordered(funcs))  # put shallowest function first
                    f1 = funcs[0]
                    t = Dummy('t')
                    # perform the substitution
                    ftry = f_num.subs(f1, t)

                    # if no Functions left, we can proceed with usual solve
                    if not ftry.has(symbol):
                        cv_sols = _solve(ftry, t, **flags)
                        cv_inv = list(ordered(_vsolve(t - f1, symbol, **flags)))[0]
                        result = [{symbol: cv_inv.subs(sol)} for sol in cv_sols]

                if result is False:
                    msg = 'multiple generators %s' % gens

            else:
                # e.g. case where gens are exp(x), exp(-x)
                u = bases.pop()
                t = Dummy('t')
                inv = _vsolve(u - t, symbol, **flags)
                if isinstance(u, (Pow, exp)):
                    # this will be resolved by factor in _tsolve but we might
                    # as well try a simple expansion here to get things in
                    # order so something like the following will work now without
                    # having to factor:
                    #
                    # >>> eq = (exp(I*(-x-2))+exp(I*(x+2)))
                    # >>> eq.subs(exp(x),y)  # fails
                    # exp(I*(-x - 2)) + exp(I*(x + 2))
                    # >>> eq.expand().subs(exp(x),y)  # works
                    # y**I*exp(2*I) + y**(-I)*exp(-2*I)
                    def _expand(p):
                        b, e = p.as_base_exp()
                        e = expand_mul(e)
                        return expand_power_exp(b**e)
                    ftry = f_num.replace(
                        lambda w: w.is_Pow or isinstance(w, exp),
                        _expand).subs(u, t)
                    if not ftry.has(symbol):
                        soln = _solve(ftry, t, **flags)
                        result = [{symbol: i.subs(s)} for i in inv for s in soln]

        elif len(gens) == 1:

            # There is only one generator that we are interested in, but
            # there may have been more than one generator identified by
            # polys (e.g. for symbols other than the one we are interested
            # in) so recast the poly in terms of our generator of interest.
            # Also use composite=True with f_num since Poly won't update
            # poly as documented in issue 8810.

            poly = Poly(f_num, gens[0], composite=True)

            # if we aren't on the tsolve-pass, use roots
            if not flags.pop('tsolve', False):
                soln = None
                deg = poly.degree()
                flags['tsolve'] = True
                hints = ('cubics', 'quartics', 'quintics')
                solvers = {h: flags.get(h) for h in hints}
                soln = roots(poly, **solvers)
                if sum(soln.values()) < deg:
                    # e.g. roots(32*x**5 + 400*x**4 + 2032*x**3 +
                    #            5000*x**2 + 6250*x + 3189) -> {}
                    # so all_roots is used and RootOf instances are
                    # returned *unless* the system is multivariate
                    # or high-order EX domain.
                    try:
                        soln = poly.all_roots()
                    except NotImplementedError:
                        if not flags.get('incomplete', True):
                                raise NotImplementedError(
                                filldedent('''
    Neither high-order multivariate polynomials
    nor sorting of EX-domain polynomials is supported.
    If you want to see any results, pass keyword incomplete=True to
    solve; to see numerical values of roots
    for univariate expressions, use nroots.
    '''))
                        else:
                            pass
                else:
                    soln = list(soln.keys())

                if soln is not None:
                    u = poly.gen
                    if u != symbol:
                        try:
                            t = Dummy('t')
                            inv = _vsolve(u - t, symbol, **flags)
                            soln = {i.subs(t, s) for i in inv for s in soln}
                        except NotImplementedError:
                            # perhaps _tsolve can handle f_num
                            soln = None
                    else:
                        check = False  # only dens need to be checked
                    if soln is not None:
                        if len(soln) > 2:
                            # if the flag wasn't set then unset it since high-order
                            # results are quite long. Perhaps one could base this
                            # decision on a certain critical length of the
                            # roots. In addition, wester test M2 has an expression
                            # whose roots can be shown to be real with the
                            # unsimplified form of the solution whereas only one of
                            # the simplified forms appears to be real.
                            flags['simplify'] = flags.get('simplify', False)
                if soln is not None:
                    result = [{symbol: v} for v in soln]

    # fallback if above fails
    # -----------------------
    if result is False:
        # try unrad
        if flags.pop('_unrad', True):
            try:
                u = unrad(f_num, symbol)
            except (ValueError, NotImplementedError):
                u = False
            if u:
                eq, cov = u
                if cov:
                    isym, ieq = cov
                    inv = _vsolve(ieq, symbol, **flags)[0]
                    rv = {inv.subs(xi) for xi in _solve(eq, isym, **flags)}
                else:
                    try:
                        rv = set(_vsolve(eq, symbol, **flags))
                    except NotImplementedError:
                        rv = None
                if rv is not None:
                    result = [{symbol: v} for v in rv]
                    # if the flag wasn't set then unset it since unrad results
                    # can be quite long or of very high order
                    flags['simplify'] = flags.get('simplify', False)
            else:
                pass  # for coverage

    # try _tsolve
    if result is False:
        flags.pop('tsolve', None)  # allow tsolve to be used on next pass
        try:
            soln = _tsolve(f_num, symbol, **flags)
            if soln is not None:
                result = [{symbol: v} for v in soln]
        except PolynomialError:
            pass
    # ----------- end of fallback ----------------------------

    if result is False:
        raise NotImplementedError('\n'.join([msg, not_impl_msg % f]))

    result = _remove_duplicate_solutions(result)

    if flags.get('simplify', True):
        result = [{k: d[k].simplify() for k in d} for d in result]
        # Simplification might reveal more duplicates
        result = _remove_duplicate_solutions(result)
        # we just simplified the solution so we now set the flag to
        # False so the simplification doesn't happen again in checksol()
        flags['simplify'] = False

    if checkdens:
        # reject any result that makes any denom. affirmatively 0;
        # if in doubt, keep it
        dens = _simple_dens(f, symbols)
        result = [r for r in result if
                  not any(checksol(d, r, **flags)
                          for d in dens)]
    if check:
        # keep only results if the check is not False
        result = [r for r in result if
                  checksol(f_num, r, **flags) is not False]
    return result


def _solve(func):
    """
    Solve func(nc) = 0.  func must be an increasing function.
    """
    # We could just as well call the variable `x` instead of `nc`, but we
    # always call this function with functions for which nc (the noncentrality
    # parameter) is the variable for which we are solving.
    nc = 1.0
    value = func(nc)
    if value == 0:
        return nc

    # Multiplicative factor by which to increase or decrease nc when
    # searching for a bracketing interval.
    factor = 2.0
    # Find a bracketing interval.
    if value > 0:
        nc /= factor
        while func(nc) > 0:
            nc /= factor
        lo = nc
        hi = factor*nc
    else:
        nc *= factor
        while func(nc) < 0:
            nc *= factor
        lo = nc/factor
        hi = nc

    # lo and hi bracket the solution for nc.
    nc = brentq(func, lo, hi, xtol=1e-13)
    return nc


def _solve(a: Array, b: Array) -> Array:
  _check_solve_shapes(a, b)

  # Broadcast leading dimensions of b to the shape of a, as is required by
  # custom_linear_solve.
  out_shape = tuple(d_a if d_b == 1 else d_b
                    for d_a, d_b in zip(a.shape[:-1] + (1,), b.shape))
  b = lax.broadcast_in_dim(b, out_shape, range(b.ndim))

  # With custom_linear_solve, we can reuse the same factorization when
  # computing sensitivities. This is considerably faster.
  lu_, _, permutation = lu(lax.stop_gradient(a))
  custom_solve = partial(
      control_flow.custom_linear_solve,
      lambda x: _broadcasted_matvec(a, x),
      solve=lambda _, x: lu_solve(lu_, permutation, x, trans=0),
      transpose_solve=lambda _, x: lu_solve(lu_, permutation, x, trans=1))
  if a.ndim == b.ndim + 1:
    # b.shape == [..., m]
    return custom_solve(b)
  else:
    # b.shape == [..., m, k]
    return api.vmap(custom_solve, b.ndim - 1, max(a.ndim, b.ndim) - 1)(b)


def _solve(a: ArrayLike, b: ArrayLike, assume_a: str, lower: bool) -> Array:
  if assume_a != 'pos':
    return jnp_linalg.solve(a, b)

  a, b = promote_dtypes_inexact(jnp.asarray(a), jnp.asarray(b))
  lax_linalg._check_solve_shapes(a, b)

  # With custom_linear_solve, we can reuse the same factorization when
  # computing sensitivities. This is considerably faster.
  factors = cho_factor(lax.stop_gradient(a), lower=lower)
  custom_solve = partial(
      lax.custom_linear_solve,
      lambda x: lax_linalg._broadcasted_matvec(a, x),
      solve=lambda _, x: cho_solve(factors, x),
      symmetric=True)
  if a.ndim == b.ndim + 1:
    # b.shape == [..., m]
    return custom_solve(b)
  else:
    # b.shape == [..., m, k]
    return vmap(custom_solve, b.ndim - 1, max(a.ndim, b.ndim) - 1)(b)


def _solve(tent, axisLimit, negative=False):
    axisMin, axisDef, axisMax, _distanceNegative, _distancePositive = axisLimit
    lower, peak, upper = tent

    # Mirror the problem such that axisDef <= peak
    if axisDef > peak:
        return [
            (scalar, _reverse_negate(t) if t is not None else None)
            for scalar, t in _solve(
                _reverse_negate(tent),
                axisLimit.reverse_negate(),
                not negative,
            )
        ]
    # axisDef <= peak

    # case 1: The whole deltaset falls outside the new limit; we can drop it
    #
    #                                          peak
    #  1.........................................o..........
    #                                           / \
    #                                          /   \
    #                                         /     \
    #                                        /       \
    #  0---|-----------|----------|-------- o         o----1
    #    axisMin     axisDef    axisMax   lower     upper
    #
    if axisMax <= lower and axisMax < peak:
        return []  # No overlap

    # case 2: Only the peak and outermost bound fall outside the new limit;
    # we keep the deltaset, update peak and outermost bound and and scale deltas
    # by the scalar value for the restricted axis at the new limit, and solve
    # recursively.
    #
    #                                  |peak
    #  1...............................|.o..........
    #                                  |/ \
    #                                  /   \
    #                                 /|    \
    #                                / |     \
    #  0--------------------------- o  |      o----1
    #                           lower  |      upper
    #                                  |
    #                                axisMax
    #
    # Convert to:
    #
    #  1............................................
    #                                  |
    #                                  o peak
    #                                 /|
    #                                /x|
    #  0--------------------------- o  o upper ----1
    #                           lower  |
    #                                  |
    #                                axisMax
    if axisMax < peak:
        mult = supportScalar({"tag": axisMax}, {"tag": tent})
        tent = (lower, axisMax, axisMax)
        return [(scalar * mult, t) for scalar, t in _solve(tent, axisLimit)]

    # lower <= axisDef <= peak <= axisMax

    gain = supportScalar({"tag": axisDef}, {"tag": tent})
    out = [(gain, None)]

    # First, the positive side

    # outGain is the scalar of axisMax at the tent.
    outGain = supportScalar({"tag": axisMax}, {"tag": tent})

    # Case 3a: Gain is more than outGain. The tent down-slope crosses
    # the axis into negative. We have to split it into multiples.
    #
    #                      | peak  |
    #  1...................|.o.....|..............
    #                      |/x\_   |
    #  gain................+....+_.|..............
    #                     /|    |y\|
    #  ................../.|....|..+_......outGain
    #                   /  |    |  | \
    #  0---|-----------o   |    |  |  o----------1
    #    axisMin    lower  |    |  |   upper
    #                      |    |  |
    #                axisDef    |  axisMax
    #                           |
    #                      crossing
    if gain >= outGain:
        # Note that this is the branch taken if both gain and outGain are 0.

        # Crossing point on the axis.
        crossing = peak + (1 - gain) * (upper - peak)

        loc = (max(lower, axisDef), peak, crossing)
        scalar = 1

        # The part before the crossing point.
        out.append((scalar - gain, loc))

        # The part after the crossing point may use one or two tents,
        # depending on whether upper is before axisMax or not, in one
        # case we need to keep it down to eternity.

        # Case 3a1, similar to case 1neg; just one tent needed, as in
        # the drawing above.
        if upper >= axisMax:
            loc = (crossing, axisMax, axisMax)
            scalar = outGain

            out.append((scalar - gain, loc))

        # Case 3a2: Similar to case 2neg; two tents needed, to keep
        # down to eternity.
        #
        #                      | peak             |
        #  1...................|.o................|...
        #                      |/ \_              |
        #  gain................+....+_............|...
        #                     /|    | \xxxxxxxxxxy|
        #                    / |    |  \_xxxxxyyyy|
        #                   /  |    |    \xxyyyyyy|
        #  0---|-----------o   |    |     o-------|--1
        #    axisMin    lower  |    |      upper  |
        #                      |    |             |
        #                axisDef    |             axisMax
        #                           |
        #                      crossing
        else:
            # A tent's peak cannot fall on axis default. Nudge it.
            if upper == axisDef:
                upper += EPSILON

            # Downslope.
            loc1 = (crossing, upper, axisMax)
            scalar1 = 0

            # Eternity justify.
            loc2 = (upper, axisMax, axisMax)
            scalar2 = 0

            out.append((scalar1 - gain, loc1))
            out.append((scalar2 - gain, loc2))

    else:
        # Special-case if peak is at axisMax.
        if axisMax == peak:
            upper = peak

        # Case 3:
        # We keep delta as is and only scale the axis upper to achieve
        # the desired new tent if feasible.
        #
        #                        peak
        #  1.....................o....................
        #                       / \_|
        #  ..................../....+_.........outGain
        #                     /     | \
        #  gain..............+......|..+_.............
        #                   /|      |  | \
        #  0---|-----------o |      |  |  o----------1
        #    axisMin    lower|      |  |   upper
        #                    |      |  newUpper
        #              axisDef      axisMax
        #
        newUpper = peak + (1 - gain) * (upper - peak)
        assert axisMax <= newUpper  # Because outGain > gain
        # Disabled because ots doesn't like us:
        # https://github.com/fonttools/fonttools/issues/3350
        if False and newUpper <= axisDef + (axisMax - axisDef) * 2:
            upper = newUpper
            if not negative and axisDef + (axisMax - axisDef) * MAX_F2DOT14 < upper:
                # we clamp +2.0 to the max F2Dot14 (~1.99994) for convenience
                upper = axisDef + (axisMax - axisDef) * MAX_F2DOT14
                assert peak < upper

            loc = (max(axisDef, lower), peak, upper)
            scalar = 1

            out.append((scalar - gain, loc))

        # Case 4: New limit doesn't fit; we need to chop into two tents,
        # because the shape of a triangle with part of one side cut off
        # cannot be represented as a triangle itself.
        #
        #            |   peak |
        #  1.........|......o.|....................
        #  ..........|...../x\|.............outGain
        #            |    |xxy|\_
        #            |   /xxxy|  \_
        #            |  |xxxxy|    \_
        #            |  /xxxxy|      \_
        #  0---|-----|-oxxxxxx|        o----------1
        #    axisMin | lower  |        upper
        #            |        |
        #          axisDef  axisMax
        #
        else:
            loc1 = (max(axisDef, lower), peak, axisMax)
            scalar1 = 1

            loc2 = (peak, axisMax, axisMax)
            scalar2 = outGain

            out.append((scalar1 - gain, loc1))
            # Don't add a dirac delta!
            if peak < axisMax:
                out.append((scalar2 - gain, loc2))

    # Now, the negative side

    # Case 1neg: Lower extends beyond axisMin: we chop. Simple.
    #
    #                     |   |peak
    #  1..................|...|.o.................
    #                     |   |/ \
    #  gain...............|...+...\...............
    #                     |x_/|    \
    #                     |/  |     \
    #                   _/|   |      \
    #  0---------------o  |   |       o----------1
    #              lower  |   |       upper
    #                     |   |
    #               axisMin   axisDef
    #
    if lower <= axisMin:
        loc = (axisMin, axisMin, axisDef)
        scalar = supportScalar({"tag": axisMin}, {"tag": tent})

        out.append((scalar - gain, loc))

    # Case 2neg: Lower is betwen axisMin and axisDef: we add two
    # tents to keep it down all the way to eternity.
    #
    #      |               |peak
    #  1...|...............|.o.................
    #      |               |/ \
    #  gain|...............+...\...............
    #      |yxxxxxxxxxxxxx/|    \
    #      |yyyyyyxxxxxxx/ |     \
    #      |yyyyyyyyyyyx/  |      \
    #  0---|-----------o   |       o----------1
    #    axisMin    lower  |       upper
    #                      |
    #                    axisDef
    #
    else:
        # A tent's peak cannot fall on axis default. Nudge it.
        if lower == axisDef:
            lower -= EPSILON

        # Downslope.
        loc1 = (axisMin, lower, axisDef)
        scalar1 = 0

        # Eternity justify.
        loc2 = (axisMin, axisMin, lower)
        scalar2 = 0

        out.append((scalar1 - gain, loc1))
        out.append((scalar2 - gain, loc2))

    return out

