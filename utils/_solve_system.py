
def _solve_system(exprs, symbols, **flags):
    """return ``(linear, solution)`` where ``linear`` is True
    if the system was linear, else False; ``solution``
    is a list of dictionaries giving solutions for the symbols
    """
    if not exprs:
        return False, []

    if flags.pop('_split', True):
        # Split the system into connected components
        V = exprs
        symsset = set(symbols)
        exprsyms = {e: e.free_symbols & symsset for e in exprs}
        E = []
        sym_indices = {sym: i for i, sym in enumerate(symbols)}
        for n, e1 in enumerate(exprs):
            for e2 in exprs[:n]:
                # Equations are connected if they share a symbol
                if exprsyms[e1] & exprsyms[e2]:
                    E.append((e1, e2))
        G = V, E
        subexprs = connected_components(G)
        if len(subexprs) > 1:
            subsols = []
            linear = True
            for subexpr in subexprs:
                subsyms = set()
                for e in subexpr:
                    subsyms |= exprsyms[e]
                subsyms = sorted(subsyms, key = lambda x: sym_indices[x])
                flags['_split'] = False  # skip split step
                _linear, subsol = _solve_system(subexpr, subsyms, **flags)
                if linear:
                    linear = linear and _linear
                if not isinstance(subsol, list):
                    subsol = [subsol]
                subsols.append(subsol)
            # Full solution is cartesian product of subsystems
            sols = []
            for soldicts in product(*subsols):
                sols.append(dict(item for sd in soldicts
                    for item in sd.items()))
            return linear, sols

    polys = []
    dens = set()
    failed = []
    result = []
    solved_syms = []
    linear = True
    manual = flags.get('manual', False)
    checkdens = check = flags.get('check', True)

    for j, g in enumerate(exprs):
        dens.update(_simple_dens(g, symbols))
        i, d = _invert(g, *symbols)
        if d in symbols:
            if linear:
                linear = solve_linear(g, 0, [d])[0] == d
        g = d - i
        g = g.as_numer_denom()[0]
        if manual:
            failed.append(g)
            continue

        poly = g.as_poly(*symbols, extension=True)

        if poly is not None:
            polys.append(poly)
        else:
            failed.append(g)

    if polys:
        if all(p.is_linear for p in polys):
            n, m = len(polys), len(symbols)
            matrix = zeros(n, m + 1)

            for i, poly in enumerate(polys):
                for monom, coeff in poly.terms():
                    try:
                        j = monom.index(1)
                        matrix[i, j] = coeff
                    except ValueError:
                        matrix[i, m] = -coeff

            # returns a dictionary ({symbols: values}) or None
            if flags.pop('particular', False):
                result = minsolve_linear_system(matrix, *symbols, **flags)
            else:
                result = solve_linear_system(matrix, *symbols, **flags)
            result = [result] if result else []
            if failed:
                if result:
                    solved_syms = list(result[0].keys())  # there is only one result dict
                else:
                    solved_syms = []
            # linear doesn't change
        else:
            linear = False
            if len(symbols) > len(polys):

                free = set().union(*[p.free_symbols for p in polys])
                free = list(ordered(free.intersection(symbols)))
                got_s = set()
                result = []
                for syms in subsets(free, min(len(free), len(polys))):
                    try:
                        # returns [], None or list of tuples
                        res = solve_poly_system(polys, *syms)
                        if res:
                            for r in set(res):
                                skip = False
                                for r1 in r:
                                    if got_s and any(ss in r1.free_symbols
                                           for ss in got_s):
                                        # sol depends on previously
                                        # solved symbols: discard it
                                        skip = True
                                if not skip:
                                    got_s.update(syms)
                                    result.append(dict(list(zip(syms, r))))
                    except NotImplementedError:
                        pass
                if got_s:
                    solved_syms = list(got_s)
                else:
                    failed.extend([g.as_expr() for g in polys])
            else:
                try:
                    result = solve_poly_system(polys, *symbols)
                    if result:
                        solved_syms = symbols
                        result = [dict(list(zip(solved_syms, r))) for r in set(result)]
                except NotImplementedError:
                    failed.extend([g.as_expr() for g in polys])
                    solved_syms = []

    # convert None or [] to [{}]
    result = result or [{}]

    if failed:
        linear = False
        # For each failed equation, see if we can solve for one of the
        # remaining symbols from that equation. If so, we update the
        # solution set and continue with the next failed equation,
        # repeating until we are done or we get an equation that can't
        # be solved.
        def _ok_syms(e, sort=False):
            rv = e.free_symbols & legal

            # Solve first for symbols that have lower degree in the equation.
            # Ideally we want to solve firstly for symbols that appear linearly
            # with rational coefficients e.g. if e = x*y + z then we should
            # solve for z first.
            def key(sym):
                ep = e.as_poly(sym)
                if ep is None:
                    complexity = (S.Infinity, S.Infinity, S.Infinity)
                else:
                    coeff_syms = ep.LC().free_symbols
                    complexity = (ep.degree(), len(coeff_syms & rv), len(coeff_syms))
                return complexity + (default_sort_key(sym),)

            if sort:
                rv = sorted(rv, key=key)
            return rv

        legal = set(symbols)  # what we are interested in
        # sort so equation with the fewest potential symbols is first
        u = Dummy()  # used in solution checking
        for eq in ordered(failed, lambda _: len(_ok_syms(_))):
            newresult = []
            bad_results = []
            hit = False
            for r in result:
                got_s = set()
                # update eq with everything that is known so far
                eq2 = eq.subs(r)
                # if check is True then we see if it satisfies this
                # equation, otherwise we just accept it
                if check and r:
                    b = checksol(u, u, eq2, minimal=True)
                    if b is not None:
                        # this solution is sufficient to know whether
                        # it is valid or not so we either accept or
                        # reject it, then continue
                        if b:
                            newresult.append(r)
                        else:
                            bad_results.append(r)
                        continue
                # search for a symbol amongst those available that
                # can be solved for
                ok_syms = _ok_syms(eq2, sort=True)
                if not ok_syms:
                    if r:
                        newresult.append(r)
                    break  # skip as it's independent of desired symbols
                for s in ok_syms:
                    try:
                        soln = _vsolve(eq2, s, **flags)
                    except NotImplementedError:
                        continue
                    # put each solution in r and append the now-expanded
                    # result in the new result list; use copy since the
                    # solution for s is being added in-place
                    for sol in soln:
                        if got_s and any(ss in sol.free_symbols for ss in got_s):
                            # sol depends on previously solved symbols: discard it
                            continue
                        rnew = r.copy()
                        for k, v in r.items():
                            rnew[k] = v.subs(s, sol)
                        # and add this new solution
                        rnew[s] = sol
                        # check that it is independent of previous solutions
                        iset = set(rnew.items())
                        for i in newresult:
                            if len(i) < len(iset):
                                # update i with what is known
                                i_items_updated = {(k, v.xreplace(rnew)) for k, v in i.items()}
                                if not i_items_updated - iset:
                                    # this is a superset of a known solution that
                                    # is smaller
                                    break
                        else:
                            # keep it
                            newresult.append(rnew)
                    hit = True
                    got_s.add(s)
                if not hit:
                    raise NotImplementedError('could not solve %s' % eq2)
            else:
                result = newresult
                for b in bad_results:
                    if b in result:
                        result.remove(b)

    if not result:
        return False, []

    # rely on linear/polynomial system solvers to simplify
    # XXX the following tests show that the expressions
    # returned are not the same as they would be if simplify
    # were applied to this:
    #   sympy/solvers/ode/tests/test_systems/test__classify_linear_system
    #   sympy/solvers/tests/test_solvers/test_issue_4886
    # so the docs should be updated to reflect that or else
    # the following should be `bool(failed) or not linear`
    default_simplify = bool(failed)
    if flags.get('simplify', default_simplify):
        for r in result:
            for k in r:
                r[k] = simplify(r[k])
        flags['simplify'] = False  # don't need to do so in checksol now

    if checkdens:
        result = [r for r in result
            if not any(checksol(d, r, **flags) for d in dens)]

    if check and not linear:
        result = [r for r in result
            if not any(checksol(e, r, **flags) is False for e in exprs)]

    result = [r for r in result if r]
    return linear, result

