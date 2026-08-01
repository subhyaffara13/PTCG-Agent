
def _native_layer_norm(
    input: torch.Tensor,
    normalized_shape: utils.ShapeType,
    weight: torch.Tensor | None,
    bias: torch.Tensor | None,
    eps: float,
) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    if input.is_mtia:
        return NotImplemented
    # We can write a util function to update decomp table if we have more ops to fallback.
    return decomp_native_layer_norm(input, normalized_shape, weight, bias, eps)


def _native_layer_norm(
    g: jit_utils.GraphContext,
    input: _C.Value,
    normalized_shape: Sequence[int],
    weight: _C.Value,
    bias: _C.Value,
    eps: float,
) -> tuple[_C.Value, _C.Value, _C.Value]:
    return opset9.native_layer_norm(g, input, normalized_shape, weight, bias, eps)

