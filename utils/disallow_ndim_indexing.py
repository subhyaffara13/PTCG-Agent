
def disallow_ndim_indexing(result) -> None:
    """
    Helper function to disallow multi-dimensional indexing on 1D Series/Index.

    GH#27125 indexer like idx[:, None] expands dim, but we cannot do that
    and keep an index, so we used to return ndarray, which was deprecated
    in GH#30588.
    """
    if np.ndim(result) > 1:
        raise ValueError(
            "Multi-dimensional indexing (e.g. `obj[:, None]`) is no longer "
            "supported. Convert to a numpy array before indexing instead."
        )

