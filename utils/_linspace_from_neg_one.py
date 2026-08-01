
def _linspace_from_neg_one(
    num_steps: int, align_corners: bool, dtype: torch.dtype, device: torch.device
):
    if num_steps <= 1:
        return torch.tensor(0, device=device, dtype=dtype)

    a = ((num_steps - 1) / num_steps) if not align_corners else 1
    return torch.linspace(-a, a, steps=num_steps, device=device, dtype=dtype)

