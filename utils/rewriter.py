
def rewriter(condition, rewrite):
    """Strategy that rewrites an integrand."""
    def _rewriter(integral):
        integrand, symbol = integral
        debug("Integral: {} is rewritten with {} on symbol: {}".format(integrand, rewrite, symbol))
        if condition(*integral):
            rewritten = rewrite(*integral)
            if rewritten != integrand:
                substep = integral_steps(rewritten, symbol)
                if not isinstance(substep, DontKnowRule) and substep:
                    return RewriteRule(integrand, symbol, rewritten, substep)
    return _rewriter

