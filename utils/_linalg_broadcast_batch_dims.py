
def _linalg_broadcast_batch_dims(
    arg1: Tensor,
    arg2: Tensor,
) -> tuple[list[int], list[int]]:
    # broadcast the batch dimensions of arg1 and arg2.
    arg1_batch_sizes = arg1.shape[:-2]
    arg2_batch_sizes = arg2.shape[:-2]
    expand_batch_portion = _broadcast_shapes(arg1_batch_sizes, arg2_batch_sizes)

    arg1_expand_size = list(expand_batch_portion)
    arg1_expand_size += [arg1.size(-2), arg1.size(-1)]

    arg2_expand_size = list(expand_batch_portion)
    arg2_expand_size += [arg2.size(-2), arg2.size(-1)]
    return arg1_expand_size, arg2_expand_size

