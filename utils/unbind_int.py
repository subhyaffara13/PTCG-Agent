
def unbind_int(func, *args, **kwargs):
    # Note that this specializes on the length of the offsets
    _, new_kwargs = normalize_function(  # type: ignore[misc]
        func, args=args, kwargs=kwargs, normalize_to_only_use_kwargs=True
    )

    dim = new_kwargs["dim"]
    if dim != 0:
        raise RuntimeError("unbind(): only supported for NestedTensor on dim=0")

    inp = new_kwargs.pop("input")
    values = inp.values()
    offsets = inp.offsets()
    lengths = inp.lengths()
    ragged_idx = inp._ragged_idx

    def _torch_check(_lengths: list[int], _offsets: list[int] | None = None) -> None:
        # This torch._check are needed for torch.compile
        # symbolic shapes processing.
        # offsets and lengths are symbolic variables during compilation,
        # we guarantee the correct offsets/lengths correspondence:
        # sum of lengths <= total ragged_dim_size
        # every length and offset are size-like variable (allows sym shapes to reason it as [2, inf))
        # offset[i] + length[i] <= ragged_dim_size, for unbind and split dim correctness
        # offsets[i] <= ragged_dim_size

        lengths_sum = 0
        ragged_dim_size = values.shape[ragged_idx - 1]
        for i in range(len(_lengths)):
            torch._check(_lengths[i] >= 0)
            torch._check(_lengths[i] <= ragged_dim_size)

            lengths_sum += _lengths[i]
            if _offsets is not None:
                torch._check(
                    _offsets[i] + _lengths[i] <= ragged_dim_size,
                    lambda: "unbind(): nested tensor offsets and lengths do not match ragged_idx dimension",
                )
        torch._check(lengths_sum <= ragged_dim_size)

        if _offsets is not None:
            for i in range(len(_offsets)):
                torch._check(_offsets[i] >= 0)
                torch._check(_offsets[i] <= ragged_dim_size)

    if lengths is None:
        lengths_scalars = offsets.diff().tolist()
        _torch_check(lengths_scalars)

        return torch.split(values, lengths_scalars, dim=(ragged_idx - 1))

    if ragged_idx <= 0:
        raise RuntimeError(
            "unbind(): nested tensor ragged_idx out of bounds (should be >= 1)"
        )

    lengths_scalars = lengths.tolist()
    offsets_scalars = offsets.tolist()

    _torch_check(lengths_scalars, offsets_scalars)

    return [
        torch.narrow(
            values,
            dim=(ragged_idx - 1),
            start=offsets_scalars[i],
            length=lengths_scalars[i],
        )
        for i in range(lengths.shape[0])
    ]

