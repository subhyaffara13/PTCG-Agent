
def _linalg_broadcast_batch_dims_name(
    arg1: Tensor,
    arg2: Tensor,
    name: str | None,
) -> tuple[Tensor, Tensor]:
    # If there's no name we assume we don't want to check the errors
    if name:
        linearSolveCheckInputs(arg1, arg2, name)

    arg1_expand_size, arg2_expand_size = _linalg_broadcast_batch_dims(arg1, arg2)

    arg1_broadcasted = (
        arg1 if arg1_expand_size == arg1.shape else arg1.expand(arg1_expand_size)
    )
    arg2_broadcasted = (
        arg2 if arg2_expand_size == arg2.shape else arg2.expand(arg2_expand_size)
    )
    return arg1_broadcasted, arg2_broadcasted

