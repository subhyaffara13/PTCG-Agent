
def reset_torch_cache() -> None:
    """Empty the CUDA cache if a GPU is available."""
    import torch

    if torch.cuda.is_available():
        torch.cuda.empty_cache()

