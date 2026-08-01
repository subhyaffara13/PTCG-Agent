
def substitution_rule(integral):
    integrand, symbol = integral

    u_var = Dummy("u")
    substitutions = find_substitutions(integrand, symbol, u_var)
    count = 0
    if substitutions:
        debug("List of Substitution Rules")
        ways = []
        for u_func, c, substituted in substitutions:
            subrule = integral_steps(substituted, u_var)
            count = count + 1
            debug("Rule {}: {}".format(count, subrule))

            if subrule.contains_dont_know():
                continue

            if simplify(c - 1) != 0:
                _, denom = c.as_numer_denom()
                if subrule:
                    subrule = ConstantTimesRule(c * substituted, u_var, c, substituted, subrule)

                if denom.free_symbols:
                    piecewise = []
                    could_be_zero = []

                    if isinstance(denom, Mul):
                        could_be_zero = denom.args
                    else:
                        could_be_zero.append(denom)

                    for expr in could_be_zero:
                        if not fuzzy_not(expr.is_zero):
                            substep = integral_steps(manual_subs(integrand, expr, 0), symbol)

                            if substep:
                                piecewise.append((
                                    substep,
                                    Eq(expr, 0)
                                ))
                    piecewise.append((subrule, True))
                    subrule = PiecewiseRule(substituted, symbol, piecewise)

            ways.append(URule(integrand, symbol, u_var, u_func, subrule))

        if len(ways) > 1:
            return AlternativeRule(integrand, symbol, ways)
        elif ways:
            return ways[0]

