
def _grouped_mm_fallback_backward(ctx, grad_output):
    """Backward pass for `_grouped_mm_fallback`. Computes grad_input and grad_weight per expert group; offs has no gradient."""
    input, weight = ctx.saved_tensors
    grad_input = torch.zeros_like(input)
    grad_weight = torch.zeros_like(weight)

    start = 0
    # single cpu<->gpu sync point here,
    # avoids multiple syncs inside the loop
    for i, end in enumerate(ctx.offs.tolist()):
        if start == end:
            continue
        torch.mm(grad_output[start:end], weight[i].T, out=grad_input[start:end])
        torch.mm(input[start:end].T, grad_output[start:end], out=grad_weight[i])
        start = end

    return grad_input, grad_weight, None

