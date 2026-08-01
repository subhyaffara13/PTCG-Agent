
def trig_rewriter(rewrite):
    def trig_rewriter_rl(args):
        a, b, m, n, integrand, symbol = args
        rewritten = rewrite(a, b, m, n, integrand, symbol)
        if rewritten != integrand:
            return RewriteRule(integrand, symbol, rewritten, integral_steps(rewritten, symbol))
    return trig_rewriter_rl

