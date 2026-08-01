
def apply_if_callable(maybe_callable, obj, **kwargs):
    """
    Evaluate possibly callable input using obj and kwargs if it is callable,
    otherwise return as it is.

    Parameters
    ----------
    maybe_callable : possibly a callable
    obj : NDFrame
    **kwargs
    """
    if isinstance(maybe_callable, Expression):
        return maybe_callable._eval_expression(obj, **kwargs)
    elif callable(maybe_callable):
        return maybe_callable(obj, **kwargs)

    return maybe_callable

