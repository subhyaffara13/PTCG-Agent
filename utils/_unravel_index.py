
def _unravel_index(indices: Tensor, shape: int | Sequence[int]) -> Tensor:
    torch._check_type(
        not indices.is_complex()
        and not indices.is_floating_point()
        and indices.dtype != torch.bool,
        lambda: f"expected 'indices' to be integer dtype, but got {indices.dtype}",
    )

    torch._check_type(
        isinstance(shape, (int, torch.SymInt, Sequence)),
        lambda: f"expected 'shape' to be int or sequence of ints, but got {type(shape)}",
    )

    if isinstance(shape, (int, torch.SymInt)):
        shape = torch.Size([shape])  # pyrefly: ignore [bad-argument-type]
    else:
        for dim in shape:
            torch._check_type(
                isinstance(dim, (int, torch.SymInt)),
                lambda: f"expected 'shape' sequence to only contain ints, but got {type(dim)}",
            )
        shape = torch.Size(shape)

    torch._check_value(
        all(dim >= 0 for dim in shape),
        lambda: f"'shape' cannot have negative values, but got {tuple(shape)}",
    )

    coefs = list(
        reversed(
            list(
                itertools.accumulate(
                    reversed(shape[1:] + torch.Size([1])), func=operator.mul
                )
            )
        )
    )
    return indices.unsqueeze(-1).floor_divide(
        torch.tensor(coefs, device=indices.device, dtype=torch.int64)
    ) % torch.tensor(shape, device=indices.device, dtype=torch.int64)

