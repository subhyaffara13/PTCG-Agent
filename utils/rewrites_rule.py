
def rewrites_rule(integral):
    integrand, symbol = integral

    if integrand.match(1/cos(symbol)):
        rewritten = integrand.subs(1/cos(symbol), sec(symbol))
        return RewriteRule(integrand, symbol, rewritten, integral_steps(rewritten, symbol))

