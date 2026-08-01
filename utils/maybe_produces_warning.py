
def maybe_produces_warning(
    warning: type[Warning], condition: bool, **kwargs
) -> AbstractContextManager:
    """
    Return a context manager that possibly checks a warning based on the condition
    """
    if condition:
        return assert_produces_warning(warning, **kwargs)
    else:
        return nullcontext()

