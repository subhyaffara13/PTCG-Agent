
def check_significant_strides(
    a: TensorLikeType, b: TensorLikeType, *, only_cuda=True, allow_rhs_unbacked=False
) -> tuple[bool, int | None]:
    return _check_strides_helper(
        a,
        b,
        only_cuda=only_cuda,
        significant_only=True,
        allow_rhs_unbacked=allow_rhs_unbacked,
    )

