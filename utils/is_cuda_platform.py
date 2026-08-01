
def is_cuda_platform() -> bool:
    if is_torch_available():
        import torch

        return getattr(torch, "version").cuda is not None
    return False

