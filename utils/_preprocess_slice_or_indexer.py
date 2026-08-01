
def _preprocess_slice_or_indexer(
    slice_or_indexer: slice | np.ndarray, length: int, allow_fill: bool
):
    if isinstance(slice_or_indexer, slice):
        return (
            "slice",
            slice_or_indexer,
            libinternals.slice_len(slice_or_indexer, length),
        )
    else:
        if (
            not isinstance(slice_or_indexer, np.ndarray)
            or slice_or_indexer.dtype.kind != "i"
        ):
            dtype = getattr(slice_or_indexer, "dtype", None)
            raise TypeError(type(slice_or_indexer), dtype)

        indexer = ensure_platform_int(slice_or_indexer)
        if not allow_fill:
            indexer = maybe_convert_indices(indexer, length)
        return "fancy", indexer, len(indexer)

