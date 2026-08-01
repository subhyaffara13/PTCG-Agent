
def proxy_rewriter(condition, rewrite):
    """Strategy that rewrites an integrand based on some other criteria."""
    def _proxy_rewriter(criteria):
        criteria, integral = criteria
        integrand, symbol = integral
        debug("Integral: {} is rewritten with {} on symbol: {} and criteria: {}".format(integrand, rewrite, symbol, criteria))
        args = criteria + list(integral)
        if condition(*args):
            rewritten = rewrite(*args)
            if rewritten != integrand:
                return RewriteRule(integrand, symbol, rewritten, integral_steps(rewritten, symbol))
    return _proxy_rewriter

