
def _aten_max_pool_with_indices_onnx(
    g: jit_utils.GraphContext,
    self: _C.Value,
    kernel_shape: Sequence[int],
    strides: Sequence[int],
    pads: Sequence[int],
    dilations: Sequence[int],
    ceil_mode: bool,
    unbatched_rank: int,
    n_dims_one: Sequence[int],
    n_dims_zero: Sequence[int],
    n_dims_axes: Sequence[int],
) -> tuple[_C.Value, Sequence[int]]:
    self_rank = g.op("Size", g.op("Shape", self))
    if self_rank == unbatched_rank:  # C,H,W -> N,C,H,W and N=1
        self = g.op(
            "Unsqueeze",
            self,
            g.op("Constant", value_t=torch.tensor([0], dtype=torch.int64)),
        )

    pool_result, indices = g.op(
        "MaxPool",
        self,
        outputs=2,
        ceil_mode_i=ceil_mode,
        dilations_i=dilations,
        kernel_shape_i=kernel_shape,
        pads_i=pads,
        strides_i=strides,
    )
    _, flatten_indices = g.op(
        "MaxPool",
        self,
        outputs=2,
        dilations_i=dilations,
        kernel_shape_i=n_dims_one,
        strides_i=n_dims_one,
    )

    ends = g.op("Constant", value_t=torch.tensor(n_dims_one))
    starts = g.op("Constant", value_t=torch.tensor(n_dims_zero))
    axes = g.op("Constant", value_t=torch.tensor(n_dims_axes))

    delta = g.op("Slice", flatten_indices, starts, ends, axes)
    indices = g.op("Sub", indices, delta)

    if self_rank == unbatched_rank:
        pool_result = g.op(
            "Squeeze", pool_result, value_t=torch.tensor([0], dtype=torch.int64)
        )
        indices = g.op("Squeeze", indices, value_t=torch.tensor([0], dtype=torch.int64))

    return (pool_result, indices)

