
def _infer_fake_from_real_tensor(
    mode: FakeTensorMode, op: torch._ops.OpOverload, real_out: torch.Tensor
) -> torch.Tensor:
    def unsupported(reason: str) -> None:
        raise RuntimeError(
            f"propagate_real_tensors: we cannot infer a Fake kernel "
            f"(meta kernel) for operator {op._name} because {reason}. "
            f"Please use torch.library.register_fake to add a Fake kernel."
        )

    if real_out.storage_offset() != 0:
        unsupported(
            f"a return has a non-zero storage offset {real_out.storage_offset()}"
        )

    # Since PT2 is rank specialized, there's no such thing as a symbolic
    # output rank. So we can assume the fake tensor has the same number of
    # dimensions as the real tensor output.
    #
    # We shouldn't assume the Fake sizes/strides are exactly what we see on
    # the real tensor output (perhaps we should give users a lever to toggle
    # this). This is because there's a good amount of operators that return
    # outputs with data-dependent output shape.
    # So we infer the output sizes to all be unbacked symints
    fake_shape = [
        torch._library.fake_impl.allocate_size(mode.shape_env)
        for _ in range(real_out.dim())
    ]

    # We infer what the strides are. We had a couple of options for this:
    # - assume the strides are computable from the sizes
    # - use new fresh unbacked symints in the strides
    #   This doesn't work that well (PT2 doesn't support unbacked symint strides well)
    # - use the real strides
    #   This can only be used if we assume the strides are static.
    # We went with the first option.
    fake_strides = [-1] * real_out.dim()
    strides = [(s, idx) for idx, s in enumerate(real_out.stride())]
    strides.sort(key=lambda x: (x[0], -x[1]))
    expected = 1
    fake_stride = expected
    for s, idx in strides:
        if s != expected:
            unsupported(
                f"a return was not dense in memory (sizes {real_out.shape} strides {real_out.stride()})"
            )
        fake_strides[idx] = fake_stride
        expected = expected * real_out.shape[idx]
        fake_stride = fake_stride * fake_shape[idx]

    with mode:
        return torch.empty_strided(
            fake_shape,
            fake_strides,
            device=real_out.device,
            dtype=real_out.dtype,
            layout=real_out.layout,
        )

