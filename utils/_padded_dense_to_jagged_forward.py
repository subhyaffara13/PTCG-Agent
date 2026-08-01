
def _padded_dense_to_jagged_forward(
    fake_mode: FakeTensorMode,
    func: OpOverload,
    padded: FakeTensor,
    offsets: list[FakeTensor],
    total_L: IntLikeType | None = None,
) -> FakeTensor:
    # only one jagged dim is supported for now
    if len(offsets) != 1:
        raise AssertionError(
            f"Only one jagged dim is supported, got {len(offsets)} offsets"
        )

    if not total_L:
        if (
            fake_mode.shape_env is None
            or not fake_mode.shape_env.allow_dynamic_output_shape_ops
        ):
            # Without symints/symfloats, cannot handle this
            raise DynamicOutputShapeException(func)

        total_L = fake_mode.shape_env.create_unbacked_symint()

        maxval = sys.maxsize - 1

        # Avoid importing sympy at a module level
        from torch.fx.experimental.symbolic_shapes import (
            _constrain_range_for_size,
            has_free_symbols,
        )

        if not has_free_symbols(padded.numel()):
            maxval = int(padded.numel())

        _constrain_range_for_size(total_L, min=0, max=maxval)

    output_shape = (total_L, *padded.shape[2:])
    return padded.new_empty(output_shape)  # type: ignore[return]

