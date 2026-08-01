
def _unsafe_masked_index(x, mask, indices, fill):
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

    from torch.fx.experimental.symbolic_shapes import guard_or_false

    if guard_or_false(x.numel() == 0):
        meta_result = torch._meta_registrations.meta_index_Tensor(x, indices)
        return x.new_full(meta_result.shape, fill)

    for i in range(len(indices)):
        index = indices[i]
        if index is not None:
            indices[i] = index.clamp(min=0, max=x.size(i) - 1)

    return aten._unsafe_index(x, indices).masked_fill(~mask, fill)


def _unsafe_masked_index(self, mask, indices, fill):
    ranges, _, _unsafe_index_fn = index_impl_helper(
        self, indices, check=False, wrap_neg=False
    )
    mask_loader = mask.make_loader()
    self_loader = self.make_loader()

    def inner_fn(idx):
        if mask.dtype != torch.bool:
            mask_val = ops.to_dtype(mask_loader(idx), torch.bool)
        else:
            mask_val = mask_loader(idx)
        return ops.masked(mask_val, lambda: self_loader(_unsafe_index_fn(idx)), fill)

    return Pointwise.create(
        device=self.get_device(),
        dtype=self.get_dtype(),
        inner_fn=inner_fn,
        ranges=ranges,
    )

