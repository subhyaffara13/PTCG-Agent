
def _apply_patternbased_threeterm_simplification(Rel, patterns, func,
                                                 dominatingvalue,
                                                 replacementvalue,
                                                 measure):
    """ Apply pattern-based three-term simplification."""
    from sympy.functions.elementary.miscellaneous import Min, Max
    from sympy.core.relational import Le, Lt, _Inequality
    changed = True
    while changed and len(Rel) >= 3:
        changed = False
        # Use only > or >=
        Rel = [r.reversed if isinstance(r, (Le, Lt)) else r for r in Rel]
        # Sort based on ordered
        Rel = list(ordered(Rel))
        # Create a list of possible replacements
        results = []
        # Eq and Ne must be tested reversed as well
        rtmp = [(r, ) if isinstance(r, _Inequality) else (r, r.reversed) for r in Rel]
        # Try all combinations of possibly reversed relational
        for ((i, pi), (j, pj), (k, pk)) in permutations(enumerate(rtmp), 3):
            for pattern, simp in patterns:
                res = []
                for p1, p2, p3 in product(pi, pj, pk):
                    # use SymPy matching
                    oldexpr = Tuple(p1, p2, p3)
                    tmpres = oldexpr.match(pattern)
                    if tmpres:
                        res.append((tmpres, oldexpr))

                if res:
                    for tmpres, oldexpr in res:
                        # we have a matching, compute replacement
                        np = simp.xreplace(tmpres)
                        if np == dominatingvalue:
                            # if dominatingvalue, the whole expression
                            # will be replacementvalue
                            return [replacementvalue]
                        # add replacement
                        if not isinstance(np, ITE) and not np.has(Min, Max):
                            # We only want to use ITE and Min/Max replacements if
                            # they simplify to a relational
                            costsaving = measure(func(*oldexpr.args)) - measure(np)
                            if costsaving > 0:
                                results.append((costsaving, ([i, j, k], np)))
        if results:
            # Sort results based on complexity
            results = sorted(results,
                                           key=lambda pair: pair[0], reverse=True)
            # Replace the one providing most simplification
            replacement = results[0][1]
            idx, newrel = replacement
            idx.sort()
            # Remove the old relationals
            for index in reversed(idx):
                del Rel[index]
            if dominatingvalue is None or newrel != Not(dominatingvalue):
                # Insert the new one (no need to insert a value that will
                # not affect the result)
                if newrel.func == func:
                    for a in newrel.args:
                        Rel.append(a)
                else:
                    Rel.append(newrel)
            # We did change something so try again
            changed = True
    return Rel

