
def _sample_njts(device, dtype, requires_grad=False, dims=None):
    if dims is None:
        dims = [2, 3, 4]
    if not isinstance(dims, (list, tuple)):
        dims = [dims]

    # contiguous NJTs
    for dim in dims:
        # with min / max seqlen cached
        shape = (_rnd(), None, *[_rnd() for _ in range(dim - 2)])
        nt = random_nt_from_dims(
            shape,
            device=device,
            dtype=dtype,
            requires_grad=requires_grad,
            layout=torch.jagged,
        )
        yield nt

        # without min / max seqlen cached
        values = _clone(nt.values())
        offsets = _clone(nt.offsets())
        yield torch.nested.nested_tensor_from_jagged(values, offsets).requires_grad_(
            requires_grad
        )

        # non-contiguous transposed NJT (not possible for 2D)
        if dim > 2:
            yield nt.transpose(-1, nt._ragged_idx)

        # non-contiguous with holes NJT
        values = _clone(nt.values())
        offsets = _clone(nt.offsets())
        # subtract 1 to cause holes
        lengths = _clone(offsets.diff() - 1)
        yield torch.nested.nested_tensor_from_jagged(
            values=values,
            offsets=offsets,
            lengths=lengths,
        ).requires_grad_(requires_grad)

