
def _init_autotune_subprocess(fp32_precision: str) -> bool:
    """
    Warmup function run in the autotune subprocess.
    """
    import torch

    # Initialize dummy tensor for CUDA context
    if torch.cuda.is_available():
        torch.zeros(1, device="cuda")

    torch.backends.cuda.matmul.fp32_precision = fp32_precision

    return True

