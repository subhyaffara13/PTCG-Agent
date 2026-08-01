
def reductify(
    grad_input: torch.Tensor | tuple[torch.Tensor, ...],
    grad_input_bdim: int | tuple[int, ...],
    input_bdim: int | tuple[int, ...],
    batch_size: int,
    target_shape_without_bdim_to_reduce_to: Any = None,
) -> tuple[Any, ...]:
    if not isinstance(grad_input, tuple):
        grad_input = (grad_input,)
    if not isinstance(grad_input_bdim, tuple):
        grad_input_bdim = (grad_input_bdim,)
    if not isinstance(input_bdim, tuple):
        input_bdim = (input_bdim,)

    if target_shape_without_bdim_to_reduce_to is None:
        target_shape_without_bdim_to_reduce_to = len(grad_input) * (None,)
    result = tuple(
        reductify_leaf(gi, gi_bdim, i_bdim, batch_size, maybe_ishape)
        for gi, gi_bdim, i_bdim, maybe_ishape in zip(
            grad_input,
            grad_input_bdim,
            input_bdim,
            target_shape_without_bdim_to_reduce_to,
        )
    )
    return result

