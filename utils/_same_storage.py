
def _same_storage(a, b):
    # Params are DTensors in backward
    # with SHARD_GRAD_OP + TP
    from torch.distributed.tensor import DTensor

    if isinstance(a, DTensor):
        a = a._local_tensor
    if isinstance(b, DTensor):
        b = b._local_tensor
    return a.untyped_storage().data_ptr() == b.untyped_storage().data_ptr()

