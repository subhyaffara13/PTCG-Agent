
def _aten_max_pool_onnx(
    g: jit_utils.GraphContext,
    self: _C.Value,
    kernel_shape: Sequence[int],
    strides: Sequence[int],
    pads: Sequence[int],
    dilations: Sequence[int],
    ceil_mode: bool,
    unbatched_rank: int,
) -> _C.Value:
    self_rank = g.op("Size", g.op("Shape", self))
    if self_rank == unbatched_rank:  # C,H,W -> N,C,H,W and N=1
        self = g.op(
            "Unsqueeze",
            self,
            g.op("Constant", value_t=torch.tensor([0], dtype=torch.int64)),
        )

    pool_result, _ = g.op(
        "MaxPool",
        self,
        outputs=2,
        ceil_mode_i=ceil_mode,
        dilations_i=dilations,
        kernel_shape_i=kernel_shape,
        pads_i=pads,
        strides_i=strides,
    )

    if self_rank == unbatched_rank:
        pool_result = g.op(
            "Squeeze",
            pool_result,
            g.op("Constant", value_t=torch.tensor([0], dtype=torch.int64)),
        )

    return pool_result

