
def has_torch_tpu() -> bool:
    """Check if torch_tpu is installed and available."""
    try:
        import torch_tpu.api  # noqa: F401  # type: ignore[import]

        # Verify hardware/runtime access
        torch_tpu.api.tpu_device()
        return True
    except (ImportError, RuntimeError):
        return False

