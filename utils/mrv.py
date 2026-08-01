
def mrv(e, x):
    """Returns a SubsSet of most rapidly varying (mrv) subexpressions of 'e',
       and e rewritten in terms of these"""
    from sympy.simplify.powsimp import powsimp
    e = powsimp(e, deep=True, combine='exp')
    if not isinstance(e, Basic):
        raise TypeError("e should be an instance of Basic")
    if not e.has(x):
        return SubsSet(), e
    elif e == x:
        s = SubsSet()
        return s, s[x]
    elif e.is_Mul or e.is_Add:
        i, d = e.as_independent(x)  # throw away x-independent terms
        if d.func != e.func:
            s, expr = mrv(d, x)
            return s, e.func(i, expr)
        a, b = d.as_two_terms()
        s1, e1 = mrv(a, x)
        s2, e2 = mrv(b, x)
        return mrv_max1(s1, s2, e.func(i, e1, e2), x)
    elif e.is_Pow and e.base != S.Exp1:
        e1 = S.One
        while e.is_Pow:
            b1 = e.base
            e1 *= e.exp
            e = b1
        if b1 == 1:
            return SubsSet(), b1
        if e1.has(x):
            return mrv(exp(e1*log(b1)), x)
        else:
            s, expr = mrv(b1, x)
            return s, expr**e1
    elif isinstance(e, log):
        s, expr = mrv(e.args[0], x)
        return s, log(expr)
    elif isinstance(e, exp) or (e.is_Pow and e.base == S.Exp1):
        # We know from the theory of this algorithm that exp(log(...)) may always
        # be simplified here, and doing so is vital for termination.
        if isinstance(e.exp, log):
            return mrv(e.exp.args[0], x)
        # if a product has an infinite factor the result will be
        # infinite if there is no zero, otherwise NaN; here, we
        # consider the result infinite if any factor is infinite
        li = limitinf(e.exp, x)
        if any(_.is_infinite for _ in Mul.make_args(li)):
            s1 = SubsSet()
            e1 = s1[e]
            s2, e2 = mrv(e.exp, x)
            su = s1.union(s2)[0]
            su.rewrites[e1] = exp(e2)
            return mrv_max3(s1, e1, s2, exp(e2), su, e1, x)
        else:
            s, expr = mrv(e.exp, x)
            return s, exp(expr)
    elif isinstance(e, AppliedUndef):
        raise ValueError("MRV set computation for UndefinedFunction is not allowed")
    elif e.is_Function:
        l = [mrv(a, x) for a in e.args]
        l2 = [s for (s, _) in l if s != SubsSet()]
        if len(l2) != 1:
            # e.g. something like BesselJ(x, x)
            raise NotImplementedError("MRV set computation for functions in"
                                      " several variables not implemented.")
        s, ss = l2[0], SubsSet()
        args = [ss.do_subs(x[1]) for x in l]
        return s, e.func(*args)
    elif e.is_Derivative:
        raise NotImplementedError("MRV set computation for derivatives"
                                  " not implemented yet.")
    raise NotImplementedError(
        "Don't know how to calculate the mrv of '%s'" % e)

