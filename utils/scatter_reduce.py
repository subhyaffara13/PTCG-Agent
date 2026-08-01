
def scatter_reduce(x, dim: int, index, src, reduction_type, **kwargs):
    return scatter_reduce_(clone(x), dim, index, src, reduction_type, **kwargs)


def scatter_reduce(
    g: jit_utils.GraphContext,
    self: torch._C.Value,
    dim: int,
    index: torch._C.Value,
    src: torch._C.Value,
    reduce: str,
    include_self: bool,
):
    if reduce == "mean":
        raise errors.OnnxExporterError(
            "ONNX does not support mean reduction for scatter_reduce"
        )
    if not include_self:
        raise errors.OnnxExporterError(
            "ONNX does not support include_self=False for scatter_reduce"
        )

    reduce_mode = {  # convert torch string name to onnx string name
        "mean": "none",  # 'mean' doesn't support in ONNX 1.14 definition
        "sum": "add",
        "prod": "mul",
        "amin": "min",
        "amax": "max",
    }
    onnx_reduce = reduce_mode[reduce]

    self_rank = g.op("Size", g.op("Shape", self))

    # if self_rank == 0:  # assert (index_rank == 0 and rank_src == 0)
    self_rank_is_zero = g.op(
        "Equal", self_rank, g.op("Constant", value_t=torch.tensor(0, dtype=torch.int64))
    )
    if_op, (if_context, else_context), _ = jit_utils.add_op_with_blocks(
        g, "If", self_rank_is_zero, n_blocks=2, outputs=3
    )
    neg_1 = if_context.op("Constant", value_t=torch.tensor([-1], dtype=torch.int64))

    self_reshape = if_context.op("Reshape", self, neg_1)
    utils._add_output_to_block(if_context.block, self_reshape)
    index_reshape = if_context.op("Reshape", index, neg_1)
    utils._add_output_to_block(if_context.block, index_reshape)
    src_reshape = if_context.op("Reshape", src, neg_1)
    utils._add_output_to_block(if_context.block, src_reshape)

    self_identity = else_context.op("Identity", self)
    utils._add_output_to_block(else_context.block, self_identity)
    index_identitye = else_context.op("Identity", index)
    utils._add_output_to_block(else_context.block, index_identitye)
    src_identity = else_context.op("Identity", src)
    utils._add_output_to_block(else_context.block, src_identity)

    result = g.op("ScatterElements", *if_op, axis_i=dim, reduction_s=onnx_reduce)

    # if self_rank == 0:
    if_op, (if_context, else_context), _ = jit_utils.add_op_with_blocks(
        g, "If", self_rank_is_zero, n_blocks=2, outputs=1
    )
    result_squeezed = if_context.op("Squeeze", result)
    utils._add_output_to_block(if_context.block, result_squeezed)
    result_identity = else_context.op("Identity", result)
    utils._add_output_to_block(else_context.block, result_identity)
    result_final = if_op.node().output()

    return result_final

