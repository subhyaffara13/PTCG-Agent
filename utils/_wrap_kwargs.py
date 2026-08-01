
def _wrap_kwargs(fun):
    """Wrap callable to accept arbitrary kwargs and ignore unused ones"""

    try:
        keys = set(inspect.signature(fun).parameters.keys())
    except ValueError:
        # NumPy Generator methods can't be inspected
        keys = {'size'}

    # Set keys=keys/fun=fun to avoid late binding gotcha
    def wrapped_rvs_i(*args, keys=keys, fun=fun, **all_kwargs):
        kwargs = {key: val for key, val in all_kwargs.items()
                  if key in keys}
        return fun(*args, **kwargs)
    return wrapped_rvs_i

