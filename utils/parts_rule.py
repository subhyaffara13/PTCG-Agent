
def parts_rule(integral):
    integrand, symbol = integral
    constant, integrand = integrand.as_coeff_Mul()

    result = _parts_rule(integrand, symbol)

    steps = []
    if result:
        u, dv, v, du, v_step = result
        debug("u : {}, dv : {}, v : {}, du : {}, v_step: {}".format(u, dv, v, du, v_step))
        steps.append(result)

        if isinstance(v, Integral):
            return

        # Set a limit on the number of times u can be used
        if isinstance(u, (sin, cos, exp, sinh, cosh)):
            cachekey = u.xreplace({symbol: _cache_dummy})
            if _parts_u_cache[cachekey] > 2:
                return
            _parts_u_cache[cachekey] += 1

        # Try cyclic integration by parts a few times
        for _ in range(4):
            debug("Cyclic integration {} with v: {}, du: {}, integrand: {}".format(_, v, du, integrand))
            coefficient = ((v * du) / integrand).cancel()
            if coefficient == 1:
                break
            if symbol not in coefficient.free_symbols:
                rule = CyclicPartsRule(integrand, symbol,
                    [PartsRule(None, None, u, dv, v_step, None)
                     for (u, dv, v, du, v_step) in steps],
                    (-1) ** len(steps) * coefficient)
                if (constant != 1) and rule:
                    rule = ConstantTimesRule(constant * integrand, symbol, constant, integrand, rule)
                return rule

            # _parts_rule is sensitive to constants, factor it out
            next_constant, next_integrand = (v * du).as_coeff_Mul()
            result = _parts_rule(next_integrand, symbol)

            if result:
                u, dv, v, du, v_step = result
                u *= next_constant
                du *= next_constant
                steps.append((u, dv, v, du, v_step))
            else:
                break

    def make_second_step(steps, integrand):
        if steps:
            u, dv, v, du, v_step = steps[0]
            return PartsRule(integrand, symbol, u, dv, v_step, make_second_step(steps[1:], v * du))
        return integral_steps(integrand, symbol)

    if steps:
        u, dv, v, du, v_step = steps[0]
        rule = PartsRule(integrand, symbol, u, dv, v_step, make_second_step(steps[1:], v * du))
        if (constant != 1) and rule:
            rule = ConstantTimesRule(constant * integrand, symbol, constant, integrand, rule)
        return rule

