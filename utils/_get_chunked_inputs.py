
def _get_chunked_inputs(
    flat_args: list[Any],
    flat_in_dims: list[int | None],
    batch_size: int,
    chunk_size: int | None,
) -> Iterable[tuple[Any, ...]]:
    split_idxs = (batch_size,)
    if chunk_size is not None:
        chunk_sizes = get_chunk_sizes(batch_size, chunk_size)
        split_idxs = tuple(itertools.accumulate(chunk_sizes))

    flat_args_chunks = tuple(
        (
            t.tensor_split(split_idxs, dim=in_dim)
            if in_dim is not None
            else [
                t,
            ]
            * len(split_idxs)
        )
        for t, in_dim in zip(flat_args, flat_in_dims)
    )

    # transpose chunk dim and flatten structure
    # chunks_flat_args is a list of flatten args
    chunks_flat_args = zip(*flat_args_chunks)
    return chunks_flat_args

