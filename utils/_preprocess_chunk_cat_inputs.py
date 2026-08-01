
def _preprocess_chunk_cat_inputs(
    tensors: list[Tensor],
    dim: int,
    num_chunks: int,
):
    torch._check(num_chunks >= 1, lambda: "_chunk_cat expects positive num_chunks")
    torch._check(
        len(tensors) > 0, lambda: "_chunk_cat expects a non-empty input tensor list"
    )
    expected_dtype = tensors[0].dtype
    expected_device = tensors[0].device
    for tensor in tensors:
        torch._check(tensor.numel() > 0, lambda: "_chunk_cat expects non-empty tensor")
        torch._check(
            tensor.dtype == expected_dtype,
            lambda: "_chunk_cat expects all input tensors with the same dtype",
        )
        torch._check(
            tensor.device == expected_device,
            lambda: "_chunk_cat expects all inputs tensors on the same device",
        )
    if have_same_ndims(tensors):
        dim = utils.canonicalize_dim(tensors[0].dim(), dim)
    else:
        torch._check(
            dim >= 0,
            lambda: "_chunk_cat expects non-negative dim when input tensors have different ndims",
        )
        for tensor in tensors:
            torch._check(
                dim < tensor.ndim,
                lambda: "_chunk_cat expects dim < ndim for all input tensors",
            )
    leading_dimension_matches(tensors, dim)
    return dim

