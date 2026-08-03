from typing import Optional

def _batch_norm_with_update(
    input: list[int],
    weight: Optional[list[int]],
    bias: Optional[list[int]],
    running_mean: Optional[list[int]],
    running_var: Optional[list[int]],
) -> tuple[list[int], list[int], list[int], list[int]]:
    _size = [input[1]]
    return _copy(input), _size, _size, [0]


def _batch_norm_with_update(
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
        True,  # training
        momentum,
        eps,
        False,  # functional
    )
    reserve = _get_batch_norm_reserve_tensor(
        input, weight, bias, running_mean, running_var, eps, training=True
    )
    return output, save_mean, save_rstd, reserve

