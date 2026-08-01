
def _batch_norm_no_update(
    input: Tensor,
    weight: Tensor | None,
    bias: Tensor | None,
    running_mean: Tensor,
    running_var: Tensor,
    momentum: float,
    eps: float,
) -> tuple[Tensor, Tensor, Tensor, Tensor]:
    output, save_mean, save_rstd, _, _ = native_batch_norm_helper(
        input,
        weight,
        bias,
        running_mean,
        running_var,
        False,  # training
        momentum,
        eps,
        False,  # functional
    )
    reserve = _get_batch_norm_reserve_tensor(
        input, weight, bias, running_mean, running_var, eps, training=False
    )
    return output, save_mean, save_rstd, reserve

