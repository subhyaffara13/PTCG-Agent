
def build_plot_signature(cls):
    """
    Decorator function for giving Plot a useful signature.

    Currently this mostly saves us some duplicated typing, but we would
    like eventually to have a way of registering new semantic properties,
    at which point dynamic signature generation would become more important.

    """
    sig = inspect.signature(cls)
    params = [
        inspect.Parameter("args", inspect.Parameter.VAR_POSITIONAL),
        inspect.Parameter("data", inspect.Parameter.KEYWORD_ONLY, default=None)
    ]
    params.extend([
        inspect.Parameter(name, inspect.Parameter.KEYWORD_ONLY, default=None)
        for name in PROPERTIES
    ])
    new_sig = sig.replace(parameters=params)
    cls.__signature__ = new_sig

    known_properties = textwrap.fill(
        ", ".join([f"|{p}|" for p in PROPERTIES]),
        width=78, subsequent_indent=" " * 8,
    )

    if cls.__doc__ is not None:  # support python -OO mode
        cls.__doc__ = cls.__doc__.format(known_properties=known_properties)

    return cls

