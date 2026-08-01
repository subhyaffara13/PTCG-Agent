
def _autograd_grad_for_inputs(
    outputs: Sequence[torch.Tensor],
    inputs: Sequence[torch.Tensor],
    grad_outputs: Sequence[torch.Tensor | None] | None = None,
    retain_graph: bool = False,
    allow_unused: bool = False,
) -> tuple[torch.Tensor | None, ...]:
    """Compute input gradients, returning ``None`` for non-grad inputs."""
    # Some inputs may not be used or may not require gradients, so we filter them out
    # before calling autograd.grad and place None for those positions in the result.
    grad_indices: list[int] = []
    inputs_requiring_grad: list[torch.Tensor] = []
    for i, inp in enumerate(inputs):
        if isinstance(inp, torch.Tensor) and inp.requires_grad:
            grad_indices.append(i)
            inputs_requiring_grad.append(inp)

    if not inputs_requiring_grad:
        return tuple(None for _ in inputs)

    grads = torch.autograd.grad(
        outputs=outputs,
        inputs=inputs_requiring_grad,
        grad_outputs=grad_outputs,
        retain_graph=retain_graph,
        allow_unused=allow_unused,
    )

    result: list[torch.Tensor | None] = [None] * len(inputs)
    for idx, g in zip(grad_indices, grads, strict=True):
        result[idx] = g
    return tuple(result)

