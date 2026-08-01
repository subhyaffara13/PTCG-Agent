
def _get_gpu_count() -> int:
    return torch.cuda.device_count()

