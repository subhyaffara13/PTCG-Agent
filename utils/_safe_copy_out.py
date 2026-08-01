
def _safe_copy_out(
    *, copy_from: TensorLikeType, copy_to: TensorLikeType, exact_dtype: bool = False
):
    # Checks same device
    if not is_cpu_scalar(copy_from):
        check_copy_devices(copy_from=copy_from, copy_to=copy_to)

    # Checks safe cast
    if exact_dtype:
        torch._check(
            copy_from.dtype == copy_to.dtype,
            lambda: f"Expected out tensor to have dtype {copy_from.dtype} "
            f"but got {copy_to.dtype} instead",
        )
    else:
        torch._check(
            utils.can_safe_cast_to(cast_from=copy_from.dtype, cast_to=copy_to.dtype),
            lambda: f"Attempting to cast from {copy_from.dtype} to out tensor with dtype {copy_to.dtype}, "
            "but this can't be cast because it is not safe!",
        )

    return copy_to.copy_(copy_from)

