
def _eigenvals_mpmath(M, multiple=False):
    """Compute eigenvalues using mpmath"""
    E, _ = _eigenvals_eigenvects_mpmath(M)
    result = [_sympify(x) for x in E]
    if multiple:
        return result
    return dict(Counter(result))

