
def _native_batch_norm_legit_functional(
    input: Tensor,
    weight: Tensor | None,
    bias: Tensor | None,
    running_mean: Tensor,
    running_var: Tensor,
    training: bool,
    momentum: float,
    eps: float,
) -> tuple[Tensor, Tensor, Tensor, Tensor, Tensor]:
    (
        output,
        save_mean,
        save_rstd,
        new_running_mean,
        new_running_var,
    ) = native_batch_norm_helper(
        input, weight, bias, running_mean, running_var, training, momentum, eps, True
    )
    if new_running_mean is None:
        raise AssertionError("new_running_mean should not be None")
    if new_running_var is None:
        raise AssertionError("new_running_var should not be None")
    return output, save_mean, save_rstd, new_running_mean, new_running_var

