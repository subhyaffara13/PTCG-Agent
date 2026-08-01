
def embedding_renorm(g: jit_utils.GraphContext, weight, indices, max_norm, norm_type):
    unique_indices = g.op("Unique", indices)
    partial_weight = g.op("Gather", weight, unique_indices)
    norm_i = int(norm_type)
    if norm_i == 1:
        norm_type = "ReduceL1"
    elif norm_i == 2:
        norm_type = "ReduceL2"
    else:
        raise errors.SymbolicValueError(
            f"Unsupported: ONNX export of embedding_renorm with norm: {norm_i}. "
            "Only 1. and 2. are supported.",
            weight,
        )
    partial_weight_norm = g.op(norm_type, partial_weight, axes_i=[1], keepdims_i=1)
    # https://github.com/pytorch/pytorch/blob/0a07488ed2c47765e337e290bd138c0e6e459cbd/aten/src/ATen/native/Embedding.cpp#L177
    # Add 1e-7 to prevent division by zero.
    partial_weight_norm_ = g.op(
        "Add", partial_weight_norm, g.op("Constant", value_t=torch.tensor(1e-7))
    )
    max_norm = torch.tensor(max_norm)
    scales = g.op("Div", max_norm, partial_weight_norm_)
    partial_weight_renorm = g.op("Mul", partial_weight, scales)
    partial_weight_renorm = g.op(
        "Where",
        g.op("Greater", partial_weight_norm, max_norm),
        partial_weight_renorm,
        partial_weight,
    )
    return g.op(
        "ScatterND",
        weight,
        symbolic_helper._unsqueeze_helper(g, unique_indices, [1]),
        partial_weight_renorm,
    )

