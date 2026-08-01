
def _ensure_single_chunk(x: Array, axis: int) -> tuple[Array, Callable[[Array], Array]]:
    """
    Make sure that Array is not broken into multiple chunks along axis.

    Returns
    -------
    x : Array
        The input Array with a single chunk along axis.
    restore : Callable[Array, Array]
        function to apply to the output to rechunk it back into reasonable chunks
    """
    if axis < 0:
        axis += x.ndim
    if x.numblocks[axis] < 2:
        return x, lambda x: x

    # Break chunks on other axes in an attempt to keep chunk size low
    x = x.rechunk({i: -1 if i == axis else "auto" for i in range(x.ndim)})

    # Rather than reconstructing the original chunks, which can be a
    # very expensive affair, just break down oversized chunks without
    # incurring in any transfers over the network.
    # This has the downside of a risk of overchunking if the array is
    # then used in operations against other arrays that match the
    # original chunking pattern.
    return x, lambda x: x.rechunk()

