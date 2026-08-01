
def clone_me(x: torch.Tensor | None) -> torch.Tensor | None:
    if x is None:
        return None
    return x.detach().clone().requires_grad_(x.requires_grad)

