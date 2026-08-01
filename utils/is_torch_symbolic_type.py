
def is_torch_symbolic_type(
    value: Any,
) -> TypeIs[torch.SymBool | torch.SymInt | torch.SymFloat]:
    return isinstance(value, (torch.SymBool, torch.SymInt, torch.SymFloat))

