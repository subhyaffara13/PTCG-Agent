
def set_torch_seed(seed: int) -> None:
    """Set the PyTorch random seed for reproducible generation."""
    import torch

    torch.manual_seed(seed)

