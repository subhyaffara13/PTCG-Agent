
def logical_not_impl(self: ComplexTensor, *args: Any, **kwargs: Any) -> torch.Tensor:
    return torch.logical_not(elemwise_nonzero(self), *args, **kwargs)

