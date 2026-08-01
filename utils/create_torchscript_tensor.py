
def create_torchscript_tensor() -> torch.Tensor:
    return torch.ones((3, 3)).requires_grad_()

