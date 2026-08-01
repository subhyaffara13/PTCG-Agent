
def fast_graph_could_be_isomorphic(G1, G2):
    """
    .. deprecated:: 3.5

       `fast_graph_could_be_isomorphic` is a deprecated alias for
       `fast_could_be_isomorphic`. Use `fast_could_be_isomorphic` instead.
    """
    import warnings

    warnings.warn(
        "fast_graph_could_be_isomorphic is deprecated, use fast_could_be_isomorphic instead",
        category=DeprecationWarning,
        stacklevel=2,
    )
    return fast_could_be_isomorphic(G1, G2)

