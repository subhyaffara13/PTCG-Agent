
def native_batch_norm(
    input: list[int],
    weight: Optional[list[int]],
    bias: Optional[list[int]],
    running_mean: Optional[list[int]],
    running_var: Optional[list[int]],
    training: bool,
) -> tuple[list[int], list[int], list[int]]:
    if training:
        _size = [input[1]]
    else:
        _size = [0]
    return _copy(input), _size, _size


def native_batch_norm(
    input: Tensor,
    weight: Tensor | None,
    bias: Tensor | None,
    running_mean: Tensor | None,
    running_var: Tensor | None,
    training: bool,
    momentum: float,
    eps: float,
) -> tuple[Tensor, Tensor, Tensor]:
    output, save_mean, save_rstd, _, _ = native_batch_norm_helper(
        input, weight, bias, running_mean, running_var, training, momentum, eps, False
    )
    return output, save_mean, save_rstd

