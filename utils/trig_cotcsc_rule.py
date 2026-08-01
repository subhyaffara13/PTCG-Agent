
def trig_cotcsc_rule(integral):
    integrand, symbol = integral
    integrand = integrand.subs({
        1 / sin(symbol): csc(symbol),
        1 / tan(symbol): cot(symbol),
        cos(symbol) / tan(symbol): cot(symbol)
    })

    if any(integrand.has(f) for f in (cot, csc)):
        pattern, a, b, m, n = cotcsc_pattern(symbol)
        match = integrand.match(pattern)
        if not match:
            return

        return multiplexer({
            cotcsc_cotodd_condition: cotcsc_cotodd,
            cotcsc_csceven_condition: cotcsc_csceven
        })(tuple(
            [match.get(i, S.Zero) for i in (a, b, m, n)] +
            [integrand, symbol]))

