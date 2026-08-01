
def get_gradient_edge(tensor: torch.Tensor) -> GradientEdge:
    """Get the gradient edge for computing the gradient of the given Tensor.

    In particular, it is equivalent to call
    ``g = autograd.grad(loss, input)`` and ``g = autograd.grad(loss, get_gradient_edge(input))``.
    """
    if not tensor.requires_grad:
        raise RuntimeError(
            "It is not possible to get the gradient edge for a Tensor "
            "that does not require gradients",
        )
    grad_fn = _get_grad_fn_or_grad_acc(tensor)

    # Python-based Node are owned by the C++ side meaning the python grad_fn
    # object we hold here does NOT keep the C++ graph alive.
    # Create an ownership token by creating a new C++ node that own the graph
    # we care about here.
    token = None
    if isinstance(grad_fn, torch._C._FunctionBase):
        with torch.enable_grad():
            token = tensor.view_as(tensor).grad_fn

    # Note that output_nr default to 0 which is the right value
    # for the AccumulateGrad node.
    # pyrefly: ignore [bad-argument-type]
    return GradientEdge(grad_fn, tensor.output_nr, ownership_token=token)

