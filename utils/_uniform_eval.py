
def _uniform_eval(f1, f2, *args, modules=None,
    force_real_eval=False, has_sum=False):
    """
    Note: this is an experimental function, as such it is prone to changes.
    Please, do not use it in your code.
    """
    np = import_module('numpy')

    def wrapper_func(func, *args):
        try:
            return complex(func(*args))
        except (ZeroDivisionError, OverflowError):
            return complex(np.nan, np.nan)

    # NOTE: np.vectorize is much slower than numpy vectorized operations.
    # However, this modules must be able to evaluate functions also with
    # mpmath or sympy.
    wrapper_func = np.vectorize(wrapper_func, otypes=[complex])

    def _eval_with_sympy(err=None):
        if f2 is None:
            msg = "Impossible to evaluate the provided numerical function"
            if err is None:
                msg += "."
            else:
                msg += "because the following exception was raised:\n"
                "{}: {}".format(type(err).__name__, err)
            raise RuntimeError(msg)
        if err:
            warnings.warn(
                "The evaluation with %s failed.\n" % (
                    "NumPy/SciPy" if not modules else modules) +
                "{}: {}\n".format(type(err).__name__, err) +
                "Trying to evaluate the expression with Sympy, but it might "
                "be a slow operation."
            )
        return wrapper_func(f2, *args)

    if modules == "sympy":
        return _eval_with_sympy()

    try:
        return wrapper_func(f1, *args)
    except Exception as err:
        return _eval_with_sympy(err)

