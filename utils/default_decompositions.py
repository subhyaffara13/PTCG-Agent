
def default_decompositions() -> "CustomDecompTable":
    """
    This is the default decomposition table which contains decomposition of
    all ATEN operators to core aten opset. Use this API together with
    :func:`run_decompositions()`
    """
    return CustomDecompTable()

