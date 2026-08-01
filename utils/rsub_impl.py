
def rsub_impl(
    lhs: ComplexTensor, rhs: ComplexTensor, alpha: int | float | complex | None = None
) -> ComplexTensor:
    if alpha is None:
        return torch.sub(rhs, lhs)  # type: ignore[bad-return]
    return torch.sub(rhs, lhs, alpha=alpha)  # type: ignore[bad-return]

