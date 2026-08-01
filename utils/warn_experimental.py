
def warn_experimental(name, stacklevel=2):
    import warnings

    msg = (
        f"Call to experimental method {name}. "
        "Be aware that the function arguments can "
        "change or be removed in future versions."
    )
    warnings.warn(msg, category=UserWarning, stacklevel=stacklevel)

