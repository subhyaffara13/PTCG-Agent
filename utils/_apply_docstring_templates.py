
def _apply_docstring_templates(func: Callable[_P, _T]) -> Callable[_P, _T]:
    """Decorator that applies docstring templates to function docstring
    and returns the function instance.
    """

    doc_string = getattr(_docs, f"{func.__name__}_docstring", None)
    if doc_string is None:
        warnings.warn(
            f"No documentation string available for {func.__name__}."
            " PyTorch team should run `python tools/update_masked_docs.py`"
            " to generate the missing docstrings.",
            stacklevel=2,
        )
    else:
        func.__doc__ = doc_string

    # Expose function as public symbol
    __all__.append(func.__name__)

    return func

