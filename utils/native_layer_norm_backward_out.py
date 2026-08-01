
def native_layer_norm_backward_out(
    grad_out: Tensor,
    input: Tensor,
    normalized_shape: list[int],
    mean: Tensor,
    rstd: Tensor,
    weight: Tensor | None,
    bias: Tensor | None,
    output_mask: list[bool],
    *,
    out0: torch.Tensor,
    out1: torch.Tensor,
    out2: torch.Tensor,
) -> tuple[Tensor | None, Tensor | None, Tensor | None]:
    result = native_layer_norm_backward(
        grad_out, input, normalized_shape, mean, rstd, weight, bias, output_mask
    )
    grad_input = (out0, out1, out2)
    for i, r in enumerate(result):
        if r is not None:
            _maybe_resize_out(grad_input[i], r.shape)
            _safe_copy_out(copy_from=r, copy_to=grad_input[i], exact_dtype=True)

    return grad_input

