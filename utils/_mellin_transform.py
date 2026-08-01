
def _mellin_transform(f, x, s_, integrator=_default_integrator, simplify=True):
    """ Backend function to compute Mellin transforms. """
    # We use a fresh dummy, because assumptions on s might drop conditions on
    # convergence of the integral.
    s = _dummy('s', 'mellin-transform', f)
    F = integrator(x**(s - 1) * f, x)

    if not F.has(Integral):
        return _simplify(F.subs(s, s_), simplify), (S.NegativeInfinity, S.Infinity), S.true

    if not F.is_Piecewise:  # XXX can this work if integration gives continuous result now?
        raise IntegralTransformError('Mellin', f, 'could not compute integral')

    F, cond = F.args[0]
    if F.has(Integral):
        raise IntegralTransformError(
            'Mellin', f, 'integral in unexpected form')

    def process_conds(cond):
        """
        Turn ``cond`` into a strip (a, b), and auxiliary conditions.
        """
        from sympy.solvers.inequalities import _solve_inequality
        a = S.NegativeInfinity
        b = S.Infinity
        aux = S.true
        conds = conjuncts(to_cnf(cond))
        t = Dummy('t', real=True)
        for c in conds:
            a_ = S.Infinity
            b_ = S.NegativeInfinity
            aux_ = []
            for d in disjuncts(c):
                d_ = d.replace(
                    re, lambda x: x.as_real_imag()[0]).subs(re(s), t)
                if not d.is_Relational or \
                    d.rel_op in ('==', '!=') \
                        or d_.has(s) or not d_.has(t):
                    aux_ += [d]
                    continue
                soln = _solve_inequality(d_, t)
                if not soln.is_Relational or \
                        soln.rel_op in ('==', '!='):
                    aux_ += [d]
                    continue
                if soln.lts == t:
                    b_ = Max(soln.gts, b_)
                else:
                    a_ = Min(soln.lts, a_)
            if a_ is not S.Infinity and a_ != b:
                a = Max(a_, a)
            elif b_ is not S.NegativeInfinity and b_ != a:
                b = Min(b_, b)
            else:
                aux = And(aux, Or(*aux_))
        return a, b, aux

    conds = [process_conds(c) for c in disjuncts(cond)]
    conds = [x for x in conds if x[2] != False]
    conds.sort(key=lambda x: (x[0] - x[1], count_ops(x[2])))

    if not conds:
        raise IntegralTransformError('Mellin', f, 'no convergence found')

    a, b, aux = conds[0]
    return _simplify(F.subs(s, s_), simplify), (a, b), aux

