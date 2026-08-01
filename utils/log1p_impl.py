
def log1p_impl(self: ComplexTensor) -> ComplexTensor:
    x, y = split_complex_tensor(self)
    # TODO (hameerabbasi): The line below may have numerical issues
    return torch.log(ComplexTensor(x + 1, y))  # type: ignore[bad-return]

