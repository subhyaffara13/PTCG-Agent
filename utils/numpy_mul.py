
def numpy_mul(x: Tensor, y: Tensor) -> Tensor:
    return torch.tensor(to_numpy(x) * to_numpy(y), device=x.device)

