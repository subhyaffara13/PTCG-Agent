
def meta_local_scalar_dense(self: Tensor):
    raise RuntimeError("Tensor.item() cannot be called on meta tensors")

