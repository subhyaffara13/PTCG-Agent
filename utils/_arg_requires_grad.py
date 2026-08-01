
def _arg_requires_grad(x: torch.Tensor | None) -> bool:
    if x is not None:
        return x.requires_grad
    return False

