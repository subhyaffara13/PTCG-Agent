
def is_torch_accelerator_available() -> bool:
    if is_torch_available():
        import torch

        return hasattr(torch, "accelerator")

    return False

