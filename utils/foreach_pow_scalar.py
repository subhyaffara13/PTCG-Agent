
def foreach_pow_scalar(
    scalar: Any, exps: Sequence[bool | complex | float | int]
) -> tuple[torch.Tensor, ...]:
    return torch._foreach_pow([scalar for _ in exps], exps)

