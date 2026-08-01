
def _native_batch_norm_legit_no_stats(
    input: Tensor,
    weight: Tensor | None,
    bias: Tensor | None,
    training: bool,
    momentum: float,
    eps: float,
) -> tuple[Tensor, Tensor, Tensor]:
    output, save_mean, save_rstd, _, _ = native_batch_norm_helper(
        input, weight, bias, None, None, training, momentum, eps, False
    )
    return output, save_mean, save_rstd

