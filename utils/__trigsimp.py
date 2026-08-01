
def __trigsimp(expr, deep=False):
    """recursive helper for trigsimp"""
    from sympy.simplify.fu import TR10i

    if _trigpat is None:
        _trigpats()
    a, b, c, d, matchers_division, matchers_add, \
    matchers_identity, artifacts = _trigpat

    if expr.is_Mul:
        # do some simplifications like sin/cos -> tan:
        if not expr.is_commutative:
            com, nc = expr.args_cnc()
            expr = _trigsimp(Mul._from_args(com), deep)*Mul._from_args(nc)
        else:
            for i, (pattern, simp, ok1, ok2) in enumerate(matchers_division):
                if not _dotrig(expr, pattern):
                    continue

                newexpr = _match_div_rewrite(expr, i)
                if newexpr is not None:
                    if newexpr != expr:
                        expr = newexpr
                        break
                    else:
                        continue

                # use SymPy matching instead
                res = expr.match(pattern)
                if res and res.get(c, 0):
                    if not res[c].is_integer:
                        ok = ok1.subs(res)
                        if not ok.is_positive:
                            continue
                        ok = ok2.subs(res)
                        if not ok.is_positive:
                            continue
                    # if "a" contains any of trig or hyperbolic funcs with
                    # argument "b" then skip the simplification
                    if any(w.args[0] == res[b] for w in res[a].atoms(
                            TrigonometricFunction, HyperbolicFunction)):
                        continue
                    # simplify and finish:
                    expr = simp.subs(res)
                    break  # process below

    if expr.is_Add:
        args = []
        for term in expr.args:
            if not term.is_commutative:
                com, nc = term.args_cnc()
                nc = Mul._from_args(nc)
                term = Mul._from_args(com)
            else:
                nc = S.One
            term = _trigsimp(term, deep)
            for pattern, result in matchers_identity:
                res = term.match(pattern)
                if res is not None:
                    term = result.subs(res)
                    break
            args.append(term*nc)
        if args != expr.args:
            expr = Add(*args)
            expr = min(expr, expand(expr), key=count_ops)
        if expr.is_Add:
            for pattern, result in matchers_add:
                if not _dotrig(expr, pattern):
                    continue
                expr = TR10i(expr)
                if expr.has(HyperbolicFunction):
                    res = expr.match(pattern)
                    # if "d" contains any trig or hyperbolic funcs with
                    # argument "a" or "b" then skip the simplification;
                    # this isn't perfect -- see tests
                    if res is None or not (a in res and b in res) or any(
                        w.args[0] in (res[a], res[b]) for w in res[d].atoms(
                            TrigonometricFunction, HyperbolicFunction)):
                        continue
                    expr = result.subs(res)
                    break

        # Reduce any lingering artifacts, such as sin(x)**2 changing
        # to 1 - cos(x)**2 when sin(x)**2 was "simpler"
        for pattern, result, ex in artifacts:
            if not _dotrig(expr, pattern):
                continue
            # Substitute a new wild that excludes some function(s)
            # to help influence a better match. This is because
            # sometimes, for example, 'a' would match sec(x)**2
            a_t = Wild('a', exclude=[ex])
            pattern = pattern.subs(a, a_t)
            result = result.subs(a, a_t)

            m = expr.match(pattern)
            was = None
            while m and was != expr:
                was = expr
                if m[a_t] == 0 or \
                        -m[a_t] in m[c].args or m[a_t] + m[c] == 0:
                    break
                if d in m and m[a_t]*m[d] + m[c] == 0:
                    break
                expr = result.subs(m)
                m = expr.match(pattern)
                m.setdefault(c, S.Zero)

    elif expr.is_Mul or expr.is_Pow or deep and expr.args:
        expr = expr.func(*[_trigsimp(a, deep) for a in expr.args])

    try:
        if not expr.has(*_trigs):
            raise TypeError
        e = expr.atoms(exp)
        new = expr.rewrite(exp, deep=deep)
        if new == e:
            raise TypeError
        fnew = factor(new)
        if fnew != new:
            new = min([new, factor(new)], key=count_ops)
        # if all exp that were introduced disappeared then accept it
        if not (new.atoms(exp) - e):
            expr = new
    except TypeError:
        pass

    return expr

