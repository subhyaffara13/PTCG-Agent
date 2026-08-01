
def _wait_tensor(tensor: torch.Tensor) -> torch.Tensor:
    return torch.ops._c10d_functional.wait_tensor(tensor)

