
def miopen_batch_norm(
    input: torch.Tensor,
    weight: torch.Tensor,
    bias: torch.Tensor | None,
    running_mean: torch.Tensor | None,
    running_var: torch.Tensor | None,
    training: bool,
    exponential_average_factor: float,
    epsilon: float,
) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    a, b, c = aten.native_batch_norm(
        input,
        weight,
        bias,
        running_mean,
        running_var,
        training,
        exponential_average_factor,
        epsilon,
    )

    if training:
        return (a, b, c)
    return (
        a,
        weight.new_zeros((0,)),
        weight.new_zeros((0,)),
    )

