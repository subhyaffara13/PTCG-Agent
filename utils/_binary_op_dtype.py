
def _binary_op_dtype(
    a: TensorLikeType | NumberType, b: TensorLikeType | NumberType
) -> torch.dtype:
    if isinstance(a, TensorLike):
        return a.dtype
    if isinstance(b, TensorLike):
        return b.dtype
    return utils.type_to_dtype(type(a))

