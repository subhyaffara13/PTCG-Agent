
def _same_storage_size(a: torch.Tensor, b: int):
    return a.untyped_storage().size() // a.element_size() == b

