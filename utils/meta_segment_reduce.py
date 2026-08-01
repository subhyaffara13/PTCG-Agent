
def meta_segment_reduce(
    data: Tensor,
    reduce: str,
    *,
    lengths: Tensor | None = None,
    indices: Tensor | None = None,
    offsets: Tensor | None = None,
    axis: int = 0,
    unsafe: bool = False,
    initial=None,
) -> Tensor:
    if indices is not None:
        raise NotImplementedError(
            "segment_reduce(): indices based reduction is not supported yet."
        )

    def segment_reduce_lengths_tensor(lengths_shape):
        return torch.empty(
            lengths_shape + data.shape[axis + 1 :],
            dtype=data.dtype,
            device="meta",
            memory_format=torch.contiguous_format,
        )

    if lengths is not None:
        return segment_reduce_lengths_tensor(lengths.shape)
    # FIXME should probably check that lengths and offset aren't both set, but
    # the ATen implementation neglects this too
    if offsets is not None:
        # lengths == torch.diff(offsets)
        lengths_shape = offsets.shape[:-1] + (offsets.shape[-1] - 1,)
        return segment_reduce_lengths_tensor(lengths_shape)
    raise RuntimeError("segment_reduce(): Either lengths or offsets must be defined.")

