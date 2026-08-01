
def _unsafe_masked_index_put_accumulate(x, mask, indices, values):
    for index in indices:
        if index is not None:
            torch._check(
                index.dtype in [torch.long, torch.int],
                lambda: "tensors used as indices must be long or int tensors",
            )

    torch._check(
        mask.dtype == torch.bool,
        lambda: "tensors used as masks must be bool tensors",
    )

    if x.numel() == 0:
        return x.clone()

    for i in range(len(indices)):
        index = indices[i]
        if index is not None:
            indices[i] = index.clamp(min=-x.size(i), max=x.size(i) - 1)

    masked_value = values.masked_fill(~mask, 0)
    return aten._unsafe_index_put(x, indices, masked_value, accumulate=True)


def _unsafe_masked_index_put_accumulate(x, mask, indices, values):
    masked_value = where(mask, values, 0)
    shape = x.get_size()
    clamped_indices = [
        clamp(indices[i], -shape[i], shape[i] - 1) if indices[i] else None
        for i in range(len(indices))
    ]
    # TODO: use a masked store for this. currently only triton
    # supports masked stores and cpp backend does not.
    return _unsafe_index_put(x, clamped_indices, masked_value, accumulate=True)

