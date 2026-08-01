
def sample_inputs__unsafe_masked_index(op_info, device, dtype, requires_grad, **kwargs):
    make_arg = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)

    def make_idx(n, m, dim, d):
        view_shape = [1] * dim
        view_shape[d] = n
        return make_tensor((n,), device=device, dtype=torch.int64, low=0, high=m).view(view_shape)

    cases = [
        ((S, S), S, M),
        ((S, S), M, S),
        ((S, S, S), S, M),
    ]

    fill_value = make_tensor([], dtype=dtype, device="cpu").item()

    for c in cases:
        self_shape, high, idx_size = c
        dim = len(self_shape)
        indices = [make_idx(idx_size, high, dim, d) for d in range(dim)]
        masks = [torch.logical_and(idx >= 0, idx < self_shape[i]) for i, idx in enumerate(indices) if idx is not None]
        mask = functools.reduce(torch.logical_and, masks)
        yield SampleInput(make_arg(self_shape), mask, indices, fill_value)

        masks = [torch.logical_and(idx >= 1, idx < self_shape[i] - 1) for i, idx in enumerate(indices) if idx is not None]
        mask = functools.reduce(torch.logical_and, masks)
        yield SampleInput(make_arg(self_shape), mask, indices, fill_value)

