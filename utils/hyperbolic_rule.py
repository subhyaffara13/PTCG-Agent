
def hyperbolic_rule(integral: tuple[Expr, Symbol]):
    integrand, symbol = integral
    if isinstance(integrand, HyperbolicFunction) and integrand.args[0] == symbol:
        if integrand.func == sinh:
            return SinhRule(integrand, symbol)
        if integrand.func == cosh:
            return CoshRule(integrand, symbol)
        u = Dummy('u')
        if integrand.func == tanh:
            rewritten = sinh(symbol)/cosh(symbol)
            return RewriteRule(integrand, symbol, rewritten,
                   URule(rewritten, symbol, u, cosh(symbol), ReciprocalRule(1/u, u, u)))
        if integrand.func == coth:
            rewritten = cosh(symbol)/sinh(symbol)
            return RewriteRule(integrand, symbol, rewritten,
                   URule(rewritten, symbol, u, sinh(symbol), ReciprocalRule(1/u, u, u)))
        else:
            rewritten = integrand.rewrite(tanh)
            if integrand.func == sech:
                return RewriteRule(integrand, symbol, rewritten,
                       URule(rewritten, symbol, u, tanh(symbol/2),
                       ArctanRule(2/(u**2 + 1), u, S(2), S.One, S.One)))
            if integrand.func == csch:
                return RewriteRule(integrand, symbol, rewritten,
                       URule(rewritten, symbol, u, tanh(symbol/2),
                       ReciprocalRule(1/u, u, u)))

