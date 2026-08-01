
def check_all_strides(
    a: TensorLikeType, b: TensorLikeType, *, only_cuda=True
) -> tuple[bool, int | None]:
    return _check_strides_helper(a, b, only_cuda=only_cuda, significant_only=False)

