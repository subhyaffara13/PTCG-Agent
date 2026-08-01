
def has_cuda_pallas() -> bool:
    """Checks for a full Pallas-on-CUDA environment."""
    return has_pallas_package() and torch.cuda.is_available() and has_jax_cuda_backend()

