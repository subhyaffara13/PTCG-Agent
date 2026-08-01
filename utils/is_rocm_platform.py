
def is_rocm_platform() -> bool:
    if is_torch_available():
        import torch

        return getattr(torch, "version").hip is not None
    return False

