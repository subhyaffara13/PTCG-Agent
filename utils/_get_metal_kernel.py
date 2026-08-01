
def _get_metal_kernel():
    """Lazily load the quantization-mlx kernel from Hugging Face Hub."""
    global _metal_kernel
    if _metal_kernel is None:
        try:
            from .hub_kernels import get_kernel

            _metal_kernel = get_kernel("kernels-community/mlx-quantization-metal-kernels")
        except Exception as e:
            raise ImportError(
                f"Failed to load the quantization-mlx kernel from the Hub: {e}. "
                "Make sure you have `kernels` installed (`pip install kernels`) "
                "and are running on an Apple Silicon machine."
            ) from e
    return _metal_kernel

