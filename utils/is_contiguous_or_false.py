
def is_contiguous_or_false(a: TensorLikeType) -> bool:
    return is_contiguous(a, false_if_dde=True)

