
def accumulate_grad(x: torch.Tensor, new_grad: torch.Tensor | None) -> None:
    # polyfills according to the Gradient Layout Contract
    if new_grad is None:
        return
    new_grad_strided = torch.empty_like(x)
    new_grad_strided.copy_(new_grad)
    if x.grad is None:
        x.grad = new_grad_strided
    elif torch.is_grad_enabled():
        x.grad = x.grad + new_grad_strided
    else:
        x.grad.add_(new_grad_strided)

