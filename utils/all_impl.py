
def all_impl(self: ComplexTensor, *args: Any, **kwargs: Any) -> torch.Tensor:
    x, y = split_complex_tensor(self)
    return torch.any(x, *args, **kwargs) & torch.any(y, *args, **kwargs)

