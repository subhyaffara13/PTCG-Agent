
def untyped_storage_size(x: torch.Tensor) -> int:
    return x.untyped_storage().size()

