
def _hyperexpand(func, z, ops0=[], z0=Dummy('z0'), premult=1, prem=0,
                 rewrite='default'):
    """
    Try to find an expression for the hypergeometric function ``func``.

    Explanation
    ===========

    The result is expressed in terms of a dummy variable ``z0``. Then it
    is multiplied by ``premult``. Then ``ops0`` is applied.
    ``premult`` must be a*z**prem for some a independent of ``z``.
    """

    if z.is_zero:
        return S.One

    from sympy.simplify.simplify import simplify

    z = polarify(z, subs=False)
    if rewrite == 'default':
        rewrite = 'nonrepsmall'

    def carryout_plan(f, ops):
        C = apply_operators(f.C.subs(f.z, z0), ops,
                            make_derivative_operator(f.M.subs(f.z, z0), z0))
        C = apply_operators(C, ops0,
                            make_derivative_operator(f.M.subs(f.z, z0)
                                         + prem*eye(f.M.shape[0]), z0))

        if premult == 1:
            C = C.applyfunc(make_simp(z0))
        r = reduce(lambda s,m: s+m[0]*m[1], zip(C, f.B.subs(f.z, z0)), S.Zero)*premult
        res = r.subs(z0, z)
        if rewrite:
            res = res.rewrite(rewrite)
        return res

    # TODO
    # The following would be possible:
    # *) PFD Duplication (see Kelly Roach's paper)
    # *) In a similar spirit, try_lerchphi() can be generalised considerably.

    global _collection
    if _collection is None:
        _collection = FormulaCollection()

    debug('Trying to expand hypergeometric function ', func)

    # First reduce order as much as possible.
    func, ops = reduce_order(func)
    if ops:
        debug('  Reduced order to ', func)
    else:
        debug('  Could not reduce order.')

    # Now try polynomial cases
    res = try_polynomial(func, z0)
    if res is not None:
        debug('  Recognised polynomial.')
        p = apply_operators(res, ops, lambda f: z0*f.diff(z0))
        p = apply_operators(p*premult, ops0, lambda f: z0*f.diff(z0))
        return unpolarify(simplify(p).subs(z0, z))

    # Try to recognise a shifted sum.
    p = S.Zero
    res = try_shifted_sum(func, z0)
    if res is not None:
        func, nops, p = res
        debug('  Recognised shifted sum, reduced order to ', func)
        ops += nops

    # apply the plan for poly
    p = apply_operators(p, ops, lambda f: z0*f.diff(z0))
    p = apply_operators(p*premult, ops0, lambda f: z0*f.diff(z0))
    p = simplify(p).subs(z0, z)

    # Try special expansions early.
    if unpolarify(z) in [1, -1] and (len(func.ap), len(func.bq)) == (2, 1):
        f = build_hypergeometric_formula(func)
        r = carryout_plan(f, ops).replace(hyper, hyperexpand_special)
        if not r.has(hyper):
            return r + p

    # Try to find a formula in our collection
    formula = _collection.lookup_origin(func)

    # Now try a lerch phi formula
    if formula is None:
        formula = try_lerchphi(func)

    if formula is None:
        debug('  Could not find an origin. ',
              'Will return answer in terms of '
              'simpler hypergeometric functions.')
        formula = build_hypergeometric_formula(func)

    debug('  Found an origin: ', formula.closed_form, ' ', formula.func)

    # We need to find the operators that convert formula into func.
    ops += devise_plan(func, formula.func, z0)

    # Now carry out the plan.
    r = carryout_plan(formula, ops) + p

    return powdenest(r, polar=True).replace(hyper, hyperexpand_special)

