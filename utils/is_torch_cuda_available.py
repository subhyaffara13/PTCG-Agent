
def is_torch_cuda_available() -> bool:
    if is_torch_available():
        import torch

        return torch.cuda.is_available()
    return False

