
def mb_unwrap_functional_tensor(tensor: torch.Tensor) -> torch.Tensor:
    if isinstance(tensor, FunctionalTensor):
        return torch._from_functional_tensor(tensor.elem)
    return tensor

