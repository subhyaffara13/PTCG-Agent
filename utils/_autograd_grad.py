
def _autograd_grad(
    outputs,
    inputs,
    grad_outputs=None,
    create_graph=False,
    retain_graph=None,
    is_grads_batched=False,
):
    # Version of autograd.grad that accepts `None` in outputs and do not compute gradients for them.
    # This has the extra constraint that inputs has to be a tuple
    if not isinstance(outputs, tuple):
        raise AssertionError("Expected outputs to be a tuple")
    if grad_outputs is None:
        grad_outputs = (None,) * len(outputs)
    if not isinstance(grad_outputs, tuple):
        raise AssertionError("Expected grad_outputs to be a tuple")
    if len(outputs) != len(grad_outputs):
        raise AssertionError(
            f"Expected outputs and grad_outputs to have the same length, "
            f"but got {len(outputs)} and {len(grad_outputs)}"
        )

    new_outputs: tuple[torch.Tensor, ...] = ()
    new_grad_outputs: tuple[torch.Tensor, ...] = ()
    for out, grad_out in zip(outputs, grad_outputs):
        if out is not None and out.requires_grad:
            new_outputs += (out,)
            # pyrefly: ignore [bad-assignment]
            new_grad_outputs += (grad_out,)

    if len(new_outputs) == 0:
        # No differentiable output, we don't need to call the autograd engine
        return (None,) * len(inputs)
    else:
        return torch.autograd.grad(
            new_outputs,
            inputs,
            new_grad_outputs,
            allow_unused=True,
            create_graph=create_graph,
            retain_graph=retain_graph,
            is_grads_batched=is_grads_batched,
        )


def _autograd_grad(
    outputs: Sequence[torch.Tensor],
    inputs: Sequence[torch.Tensor],
    grad_outputs: Sequence[torch.Tensor] | None = None,
    retain_graph: bool = False,
    create_graph: bool = True,
) -> tuple[torch.Tensor, ...]:
    if grad_outputs is None:
        diff_outputs = tuple(out for out in outputs if out.requires_grad)
    else:
        result = tuple(
            (out, go) for out, go in zip(outputs, grad_outputs) if out.requires_grad
        )
        if len(result) == 0:
            diff_outputs, grad_outputs = (), ()
        else:
            diff_outputs, grad_outputs = zip(*result)
    if len(diff_outputs) == 0:
        return tuple(torch.zeros_like(inp) for inp in inputs)
    with torch._dynamo.compiled_autograd._disable():
        grad_inputs = torch.autograd.grad(
            diff_outputs,
            inputs,
            grad_outputs,
            retain_graph=retain_graph,
            create_graph=create_graph,
            allow_unused=True,
        )
    grad_inputs = tuple(
        torch.zeros_like(inp) if gi is None else gi
        for gi, inp in zip(grad_inputs, inputs)
    )
    return grad_inputs

