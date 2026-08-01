
def has_triton_stable_tma_api() -> bool:
    if has_triton_package():
        import torch

        if (
            torch.cuda.is_available()
            and torch.cuda.get_device_capability() >= (9, 0)
            and not torch.version.hip
        ) or torch.xpu.is_available():
            try:
                from triton.language import make_tensor_descriptor  # noqa: F401

                return True
            except ImportError:
                pass
    return False

