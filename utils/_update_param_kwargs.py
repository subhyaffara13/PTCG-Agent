
def _update_param_kwargs(param_kwargs, name, value):
    """Adds a kwarg with the specified name and value to the param_kwargs dict."""
    # Make name plural (e.g. devices / dtypes) if the value is composite.
    plural_name = f"{name}s"

    # Clear out old entries of the arg if any.
    if name in param_kwargs:
        del param_kwargs[name]
    if plural_name in param_kwargs:
        del param_kwargs[plural_name]

    if isinstance(value, (list, tuple)):
        param_kwargs[plural_name] = value
    elif value is not None:
        param_kwargs[name] = value

