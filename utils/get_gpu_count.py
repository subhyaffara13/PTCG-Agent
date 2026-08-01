
def get_gpu_count():
    """
    Return the number of available gpus
    """
    if is_torch_available():
        import torch

        return torch.cuda.device_count()
    else:
        return 0

