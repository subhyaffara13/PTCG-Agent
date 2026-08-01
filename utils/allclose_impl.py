
def allclose_impl(
    input: torch.Tensor,
    other: torch.Tensor,
    rtol: float = 1e-05,
    atol: float = 1e-08,
    equal_nan: bool = False,
) -> bool:
    # pyrefly: ignore [bad-return]
    return torch.all(
        torch.isclose(input, other, rtol=rtol, atol=atol, equal_nan=equal_nan)
    ).item()  # type: ignore[bad-return]

