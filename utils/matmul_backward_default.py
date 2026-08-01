
def matmul_backward_default(func, *args, **kwargs):
    _, new_kwargs = normalize_function(  # type: ignore[misc]
        func, args=args, kwargs=kwargs, normalize_to_only_use_kwargs=True
    )

    grad = new_kwargs.pop("grad")
    inp = new_kwargs.pop("input")
    other = new_kwargs.pop("other")
    grad_input_mask = new_kwargs.pop("mask")

    if grad is None:
        return (None, None)

    grad_self = None
    if grad_input_mask[0]:
        grad_self = torch.matmul(grad, other.transpose(-1, -2))

    grad_other = None
    if grad_input_mask[1]:
        grad_other = torch.matmul(inp.transpose(-1, -2), grad)

    return (grad_self, grad_other)

