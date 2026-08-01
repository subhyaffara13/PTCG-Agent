
def is_jit_tracing() -> bool:
    try:
        import torch

        return torch.jit.is_tracing()
    except Exception:
        return False

