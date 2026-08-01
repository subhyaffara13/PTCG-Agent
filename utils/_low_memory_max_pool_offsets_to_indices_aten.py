
def _low_memory_max_pool_offsets_to_indices_aten(
    offsets,
    kernel_size,
    input_size,
    stride,
    padding,
    dilation,
):
    dim = len(kernel_size)
    offsets = offsets.to(torch.int64)
    dhw_inc = _flattened_index_to_nd(offsets, kernel_size)

    idhw = []
    for d in range(dim):
        bh_shape = [1] * offsets.ndim
        bh_shape[-dim + d] = -1
        bh = torch.arange(
            offsets.shape[-dim + d], dtype=torch.int64, device=offsets.device
        ).view(bh_shape)
        hbase = bh * stride[d] - padding[d]
        idhw.append(hbase + dhw_inc[d] * dilation[d])

    return _flatten_index(idhw, input_size)

