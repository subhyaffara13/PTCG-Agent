
def linalg_vector_norm_impl(
    self: ComplexTensor, *args: Any, **kwargs: Any
) -> torch.Tensor:
    return torch.linalg.vector_norm(torch.abs(self), *args, **kwargs)

