
def _assign_default_kwargs(kws, call_func, source_func):
    """Assign default kwargs for call_func using values from source_func."""
    # This exists so that axes-level functions and figure-level functions can
    # both call a Plotter method while having the default kwargs be defined in
    # the signature of the axes-level function.
    # An alternative would be to have a decorator on the method that sets its
    # defaults based on those defined in the axes-level function.
    # Then the figure-level function would not need to worry about defaults.
    # I am not sure which is better.
    needed = inspect.signature(call_func).parameters
    defaults = inspect.signature(source_func).parameters

    for param in needed:
        if param in defaults and param not in kws:
            kws[param] = defaults[param].default

    return kws

