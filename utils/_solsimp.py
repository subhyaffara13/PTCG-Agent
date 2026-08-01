
def _solsimp(e, t):
    no_t, has_t = powsimp(expand_mul(e)).as_independent(t)

    no_t = ratsimp(no_t)
    has_t = has_t.replace(exp, lambda a: exp(factor_terms(a)))

    return no_t + has_t

