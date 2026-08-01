
def _get_grad_fn_or_grad_acc(t: Union[torch.Tensor, "GradientEdge"]) -> Node:
    if isinstance(t, GradientEdge):
        return t.node
    if t.requires_grad and t.grad_fn is None:
        with torch.enable_grad():
            node = t.view_as(t).grad_fn.next_functions[0][0]  # type: ignore[union-attr]
    else:
        node = t.grad_fn
    if node is None:
        raise AssertionError("Expected gradient function to be set")
    return node


def _get_grad_fn_or_grad_acc(t: torch.Tensor) -> Node | None:
    """
    Get the grad function or grad accumulator for a tensor.

    Accumulate grad nodes are lazily created, so we need to a
    dummy view in order to trigger its creation.
    """
    if t.requires_grad and t.grad_fn is None:
        # if no grad function (leaf tensors) we use view
        viewed_t = t.view_as(t)
        grad_fn = viewed_t.grad_fn
        if grad_fn is not None:
            return grad_fn.next_functions[0][0]
        else:
            raise RuntimeError(
                "Attempted to get grad_fn, but got None."
                "Is this being created in a no-grad context?"
            )
    else:
        return t.grad_fn

