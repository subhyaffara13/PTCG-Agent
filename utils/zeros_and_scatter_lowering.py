
def zeros_and_scatter_lowering(shape: list[int], indices, values):
    """To support backwards on captured buffers we register a specific lowering for our specific custom up"""
    # Always accumulate into fp32 then cast
    grad = _full(0, values.get_device(), torch.float32, shape)
    assert isinstance(grad, TensorBox)
    grad.realize()
    x_size = grad.get_size()
    values = to_dtype(values, grad.get_dtype())
    indices_loaders = [i.make_loader() if i is not None else None for i in indices]
    indices, tensor_indices = check_and_broadcast_indices(indices, grad.get_device())
    # We can use the first one since they are all required to be the same size
    tensor_size = list(indices[tensor_indices[0]].get_size())
    indexed_size = [x_size[i] for i in range(len(indices))]

    expected_vals_size, inner_fn = index_output_size_and_inner_fn(
        x_size,
        indices,
        tensor_indices,
        tensor_size,
        indices_loaders,
        indexed_size,
        None,
        check=True,
    )

    values = expand(values, expected_vals_size)
    device = grad.get_device()
    assert device is not None
    scatter = Scatter(
        device=device,
        dtype=grad.get_dtype(),
        inner_fn=values.make_loader(),
        ranges=expected_vals_size,  # iter_ranges,
        output_indexer=inner_fn,
        scatter_mode="atomic_add",
    )

    buffer = ComputedBuffer(
        name=grad.data.data.name,  # type: ignore[attr-defined]
        layout=MutationLayoutSHOULDREMOVE(grad),
        data=scatter,
    )
    return buffer

