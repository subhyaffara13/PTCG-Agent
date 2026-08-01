
def is_torchdynamo_compiling() -> bool:
    # Importing torch._dynamo causes issues with PyTorch profiler (https://github.com/pytorch/pytorch/issues/130622)
    # hence rather relying on `torch.compiler.is_compiling()` when possible (torch>=2.3)
    try:
        import torch

        if hasattr(torch, "compiler"):
            return torch.compiler.is_compiling()
        return False
    except Exception:
        return False

