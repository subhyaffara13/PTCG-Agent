
def _native_batch_norm_legit_no_training(
    input: Tensor,
    weight: Tensor | None,
    bias: Tensor | None,
    running_mean: Tensor,
    running_var: Tensor,
    momentum: float,
    eps: float,
) -> tuple[Tensor, Tensor, Tensor]:
    return aten._native_batch_norm_legit.default(
        input,
        weight,
        bias,
        running_mean,
        running_var,
        False,  # training
        momentum,
        eps,
    )

