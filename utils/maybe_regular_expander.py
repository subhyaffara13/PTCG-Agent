
def maybe_regular_expander(n, d, *, create_using=None, max_tries=100, seed=None):
    """
    .. deprecated:: 3.6
       `maybe_regular_expander` is a deprecated alias
       for `maybe_regular_expander_graph`.
       Use `maybe_regular_expander_graph` instead.
    """
    import warnings

    warnings.warn(
        "maybe_regular_expander is deprecated, "
        "use `maybe_regular_expander_graph` instead.",
        category=DeprecationWarning,
        stacklevel=2,
    )
    return maybe_regular_expander_graph(
        n, d, create_using=create_using, max_tries=max_tries, seed=seed
    )

