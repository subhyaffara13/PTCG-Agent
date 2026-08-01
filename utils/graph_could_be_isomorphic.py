
def graph_could_be_isomorphic(G1, G2):
    """
    .. deprecated:: 3.5

       `graph_could_be_isomorphic` is a deprecated alias for `could_be_isomorphic`.
       Use `could_be_isomorphic` instead.
    """
    import warnings

    warnings.warn(
        "graph_could_be_isomorphic is deprecated, use `could_be_isomorphic` instead.",
        category=DeprecationWarning,
        stacklevel=2,
    )
    return could_be_isomorphic(G1, G2)

