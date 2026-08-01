
def _default_input_gen_fn(fake_tensor: torch.Tensor) -> torch.Tensor:
    """Default input generator that creates a real tensor matching the fake tensor's shape."""
    return torch.randn(
        fake_tensor.shape, dtype=fake_tensor.dtype, device=fake_tensor.device
    )

