
def _laplace_expand(f, t, s):
    """
    This function tries to expand its argument with successively stronger
    methods: first it will expand on the top level, then it will expand any
    multiplications in depth, then it will try all available expansion methods,
    and finally it will try to expand trigonometric functions.

    If it can expand, it will then compute the Laplace transform of the
    expanded term.
    """

    r = expand(f, deep=False)
    if r.is_Add:
        return _laplace_transform(r, t, s, simplify=False)
    r = expand_mul(f)
    if r.is_Add:
        return _laplace_transform(r, t, s, simplify=False)
    r = expand(f)
    if r.is_Add:
        return _laplace_transform(r, t, s, simplify=False)
    if r != f:
        return _laplace_transform(r, t, s, simplify=False)
    r = expand(expand_trig(f))
    if r.is_Add:
        return _laplace_transform(r, t, s, simplify=False)
    return None

