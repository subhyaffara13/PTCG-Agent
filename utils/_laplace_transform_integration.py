
def _laplace_transform_integration(f, t, s_, *, simplify):
    """ The backend function for doing Laplace transforms by integration.

    This backend assumes that the frontend has already split sums
    such that `f` is to an addition anymore.
    """
    s = Dummy('s')

    if f.has(DiracDelta):
        return None

    F = integrate(f*exp(-s*t), (t, S.Zero, S.Infinity))

    if not F.has(Integral):
        return _simplify(F.subs(s, s_), simplify), S.NegativeInfinity, S.true

    if not F.is_Piecewise:
        return None

    F, cond = F.args[0]
    if F.has(Integral):
        return None

    def process_conds(conds):
        """ Turn ``conds`` into a strip and auxiliary conditions. """
        from sympy.solvers.inequalities import _solve_inequality
        a = S.NegativeInfinity
        aux = S.true
        conds = conjuncts(to_cnf(conds))
        p, q, w1, w2, w3, w4, w5 = symbols(
            'p q w1 w2 w3 w4 w5', cls=Wild, exclude=[s])
        patterns = (
            p*Abs(arg((s + w3)*q)) < w2,
            p*Abs(arg((s + w3)*q)) <= w2,
            Abs(periodic_argument((s + w3)**p*q, w1)) < w2,
            Abs(periodic_argument((s + w3)**p*q, w1)) <= w2,
            Abs(periodic_argument((polar_lift(s + w3))**p*q, w1)) < w2,
            Abs(periodic_argument((polar_lift(s + w3))**p*q, w1)) <= w2)
        for c in conds:
            a_ = S.Infinity
            aux_ = []
            for d in disjuncts(c):
                if d.is_Relational and s in d.rhs.free_symbols:
                    d = d.reversed
                if d.is_Relational and isinstance(d, (Ge, Gt)):
                    d = d.reversedsign
                for pat in patterns:
                    m = d.match(pat)
                    if m:
                        break
                if m and m[q].is_positive and m[w2]/m[p] == pi/2:
                    d = -re(s + m[w3]) < 0
                m = d.match(p - cos(w1*Abs(arg(s*w5))*w2)*Abs(s**w3)**w4 < 0)
                if not m:
                    m = d.match(
                        cos(p - Abs(periodic_argument(s**w1*w5, q))*w2) *
                        Abs(s**w3)**w4 < 0)
                if not m:
                    m = d.match(
                        p - cos(
                            Abs(periodic_argument(polar_lift(s)**w1*w5, q))*w2
                            )*Abs(s**w3)**w4 < 0)
                if m and all(m[wild].is_positive for wild in [
                        w1, w2, w3, w4, w5]):
                    d = re(s) > m[p]
                d_ = d.replace(
                    re, lambda x: x.expand().as_real_imag()[0]).subs(re(s), t)
                if (
                        not d.is_Relational or d.rel_op in ('==', '!=')
                        or d_.has(s) or not d_.has(t)):
                    aux_ += [d]
                    continue
                soln = _solve_inequality(d_, t)
                if not soln.is_Relational or soln.rel_op in ('==', '!='):
                    aux_ += [d]
                    continue
                if soln.lts == t:
                    return None
                else:
                    a_ = Min(soln.lts, a_)
            if a_ is not S.Infinity:
                a = Max(a_, a)
            else:
                aux = And(aux, Or(*aux_))
        return a, aux.canonical if aux.is_Relational else aux

    conds = [process_conds(c) for c in disjuncts(cond)]
    conds2 = [x for x in conds if x[1] !=
              S.false and x[0] is not S.NegativeInfinity]
    if not conds2:
        conds2 = [x for x in conds if x[1] != S.false]
    conds = list(ordered(conds2))

    def cnt(expr):
        if expr in (True, False):
            return 0
        return expr.count_ops()
    conds.sort(key=lambda x: (-x[0], cnt(x[1])))

    if not conds:
        return None
    a, aux = conds[0]  # XXX is [0] always the right one?

    def sbs(expr):
        return expr.subs(s, s_)
    if simplify:
        F = _simplifyconds(F, s, a)
        aux = _simplifyconds(aux, s, a)
    return _simplify(F.subs(s, s_), simplify), sbs(a), _canonical(sbs(aux))

