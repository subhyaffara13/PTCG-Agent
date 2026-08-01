
def postprocess_for_cse(expr, optimizations):
    """Postprocess an expression after common subexpression elimination to
    return the expression to canonical SymPy form.

    Parameters
    ==========

    expr : SymPy expression
        The target expression to transform.
    optimizations : list of (callable, callable) pairs, optional
        The (preprocessor, postprocessor) pairs.  The postprocessors will be
        applied in reversed order to undo the effects of the preprocessors
        correctly.

    Returns
    =======

    expr : SymPy expression
        The transformed expression.
    """
    for pre, post in reversed(optimizations):
        if post is not None:
            expr = post(expr)
    return expr

