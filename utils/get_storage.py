
def get_storage(t: torch.Tensor) -> int:
    return t.untyped_storage()._cdata

