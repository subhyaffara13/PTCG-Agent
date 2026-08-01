
def _repeat_interleave_single_value_repeat_helper(
    g: jit_utils.GraphContext, self, repeats, dim
):
    from torch.onnx._internal.torchscript_exporter.symbolic_opset9 import (
        flatten,
        unsqueeze,
    )

    if not _is_tensor(repeats):
        repeats = g.op("Constant", value_t=torch.LongTensor(repeats))

    const_repeats: bool = _is_constant(repeats)
    reps = _maybe_get_const(repeats, "t")

    # Convert 'repeats' to 1-d if it is 0-d.
    if _get_tensor_rank(repeats) == 0:
        repeats = g.op("Reshape", repeats, g.op("Constant", value_t=torch.tensor([1])))

    # Create a new dim of size 1, then expand it to be 'repeats' long, and finally collapse it.
    unsqueezed = unsqueeze(g, self, dim + 1)

    # repeats_per_dim is 1 for all dims except for the new unsqueezed dim, where it has value 'repeats'.
    if const_repeats:
        # 'Repeats' is a constant, 'repeats_per_dim' can be a constant.
        onehot = torch.ones(_get_tensor_rank(unsqueezed), dtype=torch.int64)  # type: ignore[arg-type]
        onehot[dim + 1] = reps
        repeats_per_dim = g.op("Constant", value_t=onehot)
    else:
        # 'Repeats' is a variable, 'repeats_per_dim' cannot be a constant.
        onehot = g.op(
            "OneHot",
            unsqueeze(g, dim + 1, 0),  # indices, must be >= 1-dimensional
            g.op(
                "Constant", value_t=torch.tensor(_get_tensor_rank(unsqueezed))
            ),  # depth
            g.op(
                "Concat", g.op("Constant", value_t=torch.tensor([1])), repeats, axis_i=0
            ),  # on/off values
        )
        repeats_per_dim = flatten(g, onehot, 0, 1)

    tiled = g.op("Tile", unsqueezed, repeats_per_dim)
    return flatten(g, tiled, dim, dim + 1)

