
def native_batch_norm_backward_out(
    grad_out: Tensor,
    input: Tensor,
    weight: Tensor | None,
    running_mean: Tensor | None,
    running_var: Tensor | None,
    save_mean: Tensor | None,
    save_invstd: Tensor | None,
    train: bool,
    eps: float,
    output_mask: list[bool],
    *,
    out0: torch.Tensor,
    out1: torch.Tensor,
    out2: torch.Tensor,
) -> tuple[Tensor, Tensor | None, Tensor | None]:
    result = native_batch_norm_backward(
        grad_out,
        input,
        weight,
        running_mean,
        running_var,
        save_mean,
        save_invstd,
        train,
        eps,
        output_mask,
    )
    grad_input = (out0, out1, out2)
    for i, r in enumerate(result):
        if r is not None:
            _maybe_resize_out(grad_input[i], r.shape)
            _safe_copy_out(copy_from=r, copy_to=grad_input[i], exact_dtype=True)

    return grad_input

