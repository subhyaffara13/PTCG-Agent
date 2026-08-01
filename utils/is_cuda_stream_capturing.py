
def is_cuda_stream_capturing() -> bool:
    try:
        import torch

        return torch.cuda.is_current_stream_capturing()
    except Exception:
        return False

