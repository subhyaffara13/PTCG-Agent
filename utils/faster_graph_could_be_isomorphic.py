
def faster_graph_could_be_isomorphic(G1, G2):
    """
    .. deprecated:: 3.5

       `faster_graph_could_be_isomorphic` is a deprecated alias for
       `faster_could_be_isomorphic`. Use `faster_could_be_isomorphic` instead.
    """
    import warnings

    warnings.warn(
        "faster_graph_could_be_isomorphic is deprecated, use faster_could_be_isomorphic instead",
        category=DeprecationWarning,
        stacklevel=2,
    )
    return faster_could_be_isomorphic(G1, G2)

