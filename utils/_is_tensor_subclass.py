
def _is_tensor_subclass(t: torch.Tensor) -> bool:
    return isinstance(t, torch.Tensor) and type(t.data) is not torch.Tensor

