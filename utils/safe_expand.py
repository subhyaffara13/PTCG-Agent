
def safe_expand(r: _SympyT) -> _SympyT:
    """
    Expand the given symbolic expression by recursively rewriting product of
    sums into sum of products (with the product being either a multiplication or
    exponentiation).

    NOTE: using this on an intermediate expression may prevent simplification
    down the line, e.g., if we eagerly expand `(a + b)^2` into `a^2 + 2ab + b^2`,
    we won't be able to simplify `(a^2 + 2ab + b^2) / (a + b)` as easily.
    """
    if hasattr(r, "expand"):
        try:
            return _fast_expand(r)
        except RecursionError:
            log.warning("RecursionError in _fast_expand(%s)", r)
            return r
    else:
        return r

