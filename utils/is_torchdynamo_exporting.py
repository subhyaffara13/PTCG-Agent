
def is_torchdynamo_exporting() -> bool:
    try:
        import torch

        if hasattr(torch, "compiler"):
            return torch.compiler.is_exporting()
        return False
    except Exception:
        return False

