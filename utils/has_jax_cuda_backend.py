
def has_jax_cuda_backend() -> bool:
    """Check if JAX has CUDA backend support with SM90+ (required by Mosaic GPU)."""
    if not has_jax_package():
        return False
    try:
        import jax  # type: ignore[import-not-found]

        # Check if CUDA backend is available
        devices = jax.devices("gpu")
        if len(devices) == 0:
            return False

        # Mosaic GPU requires SM90+ (compute capability 9.0+)
        if torch.cuda.is_available():
            major, minor = torch.cuda.get_device_capability()
            if major < 9:
                return False

        return True
    except Exception:
        return False

