
def _exp_is_pow(x):
    """
    Control whether `e^x` should be represented as ``exp(x)`` or a ``Pow(E, x)``.

    Examples
    ========

    >>> from sympy import exp
    >>> from sympy.abc import x
    >>> from sympy.core.parameters import _exp_is_pow
    >>> with _exp_is_pow(True): print(type(exp(x)))
    <class 'sympy.core.power.Pow'>
    >>> with _exp_is_pow(False): print(type(exp(x)))
    exp
    """
    old = global_parameters.exp_is_pow

    clear_cache()
    try:
        global_parameters.exp_is_pow = x
        yield
    finally:
        clear_cache()
        global_parameters.exp_is_pow = old

