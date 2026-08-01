
def random_lobster(n, p1, p2, seed=None, *, create_using=None):
    """
    .. deprecated:: 3.5
       `random_lobster` is a deprecated alias
       for `random_lobster_graph`.
       Use `random_lobster_graph` instead.
    """
    import warnings

    warnings.warn(
        "`random_lobster` is deprecated, use `random_lobster_graph` instead.",
        category=DeprecationWarning,
        stacklevel=2,
    )
    return random_lobster_graph(n, p1, p2, seed=seed, create_using=create_using)

