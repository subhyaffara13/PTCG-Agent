
def native_batch_norm_decomposition(
    input: Tensor,
    weight: Tensor | None,
    bias: Tensor | None,
    running_mean: Tensor | None,
    running_var: Tensor | None,
    training: bool,
    momentum: float,
    eps: float,
) -> tuple[Tensor, Tensor, Tensor]:
    if running_mean is None and running_var is None:
        return aten._native_batch_norm_legit(
            input, weight, bias, training, momentum, eps
        )
    if running_mean is None:
        raise RuntimeError(
            "running_mean is None, but running_var is provided. "
            "They should both be None or both be provided."
        )
    if running_var is None:
        raise RuntimeError(
            "running_var is None, but running_mean is provided. "
            "They should both be None or both be provided."
        )
    if training:
        # HACK: batch norm consolidation should clean this up so this op doesn't take in a training arg.
        return aten._native_batch_norm_legit(
            input, weight, bias, running_mean, running_var, training, momentum, eps
        )
    else:
        return aten._native_batch_norm_legit_no_training(
            input, weight, bias, running_mean, running_var, momentum, eps
        )

