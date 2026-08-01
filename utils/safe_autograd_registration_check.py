
def safe_autograd_registration_check(
    op: torch._ops.OpOverload,
    args: tuple[Any, ...],
    kwargs: dict[str, Any],
    *,
    copy_inputs: bool = True,
    rtol: float | None = None,
    atol: float | None = None,
) -> None:
    if pytree.tree_any_only(torch.Tensor, is_abstract, (args, kwargs)):
        return
    if copy_inputs:
        args, kwargs = deepcopy_tensors((args, kwargs))
    # Don't perform autograd_registration_check if none of the inputs require grad.
    if not pytree.tree_any_only(
        torch.Tensor, lambda x: x.requires_grad, (args, kwargs)
    ):
        return
    return autograd_registration_check(op, args, kwargs)

