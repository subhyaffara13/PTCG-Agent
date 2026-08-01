
def _data_ptr_allocated(tensor: torch.Tensor) -> bool:
    return tensor.untyped_storage().data_ptr() > 0

