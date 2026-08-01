
def _set_tensor_requires_grad(x: torch.Tensor) -> torch.Tensor:
    # avoid graph-break on x.requires_grad_()
    # https://github.com/pytorch/pytorch/pull/110053
    return x.requires_grad_()

