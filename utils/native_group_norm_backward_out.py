
def native_group_norm_backward_out(
    grad_output: Tensor,
    input: Tensor,
    mean: Tensor,
    rstd: Tensor,
    gamma: Tensor | None,
    N: int,
    C: int,
    HxW: int,
    group: int,
    output_mask: list[bool],
    *,
    out0: torch.Tensor,
    out1: torch.Tensor,
    out2: torch.Tensor,
) -> tuple[Tensor | None, Tensor | None, Tensor | None]:
    result = native_group_norm_backward(
        grad_output, input, mean, rstd, gamma, N, C, HxW, group, output_mask
    )
    grad_input = (out0, out1, out2)
    for i, r in enumerate(result):
        if r is not None:
            _maybe_resize_out(grad_input[i], r.shape)
            _safe_copy_out(copy_from=r, copy_to=grad_input[i], exact_dtype=True)

    return grad_input

