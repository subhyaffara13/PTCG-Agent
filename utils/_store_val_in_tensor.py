
def _store_val_in_tensor(val) -> torch.Tensor:
    # hack to get dynamic shapes support: store in a (val, 0) shaped tensor
    return torch.zeros(val, 0)

