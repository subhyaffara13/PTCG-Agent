
def _get_grad_norm(
    params: Iterable[nn.Parameter],
    norm_type: float,
    zero: torch.Tensor,
    device: torch.device,
) -> torch.Tensor:
    """
    Return the gradient norm of parameters ``param`` s, where the gradients are viewed as a single vector.

    The returned norm is in FP32 even if parameters/gradients are in a low precision. This is because the downstream
    use of this return value is a reduction across ranks.
    """
    params_with_grad = [param for param in params if param.grad is not None]
    if len(params_with_grad) == 0:
        # Reuse a tensor for zero to avoid a GPU sync
        return zero
    grads = [param.grad for param in params_with_grad]
    # Compute the gradient norm in FP32, where we treat the gradients as a
    # single vector. This naturally handles mixed-dtype gradients since we
    # cast each gradient to FP32 during the norm computation.
    grad_norm = torch.linalg.vector_norm(
        torch.stack(
            [
                torch.linalg.vector_norm(grad.detach(), norm_type, dtype=torch.float32)
                for grad in grads
            ],
        ),
        norm_type,
        dtype=torch.float32,
    )
    return grad_norm.to(device=device)

