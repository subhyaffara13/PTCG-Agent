
def trig_rule(integral):
    integrand, symbol = integral
    if integrand == sin(symbol):
        return SinRule(integrand, symbol)
    if integrand == cos(symbol):
        return CosRule(integrand, symbol)
    if integrand == sec(symbol)**2:
        return Sec2Rule(integrand, symbol)
    if integrand == csc(symbol)**2:
        return Csc2Rule(integrand, symbol)

    if isinstance(integrand, tan):
        rewritten = sin(*integrand.args) / cos(*integrand.args)
    elif isinstance(integrand, cot):
        rewritten = cos(*integrand.args) / sin(*integrand.args)
    elif isinstance(integrand, sec):
        arg = integrand.args[0]
        rewritten = ((sec(arg)**2 + tan(arg) * sec(arg)) /
                     (sec(arg) + tan(arg)))
    elif isinstance(integrand, csc):
        arg = integrand.args[0]
        rewritten = ((csc(arg)**2 + cot(arg) * csc(arg)) /
                     (csc(arg) + cot(arg)))
    else:
        return

    return RewriteRule(integrand, symbol, rewritten, integral_steps(rewritten, symbol))

