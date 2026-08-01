
def is_fake_tensor(x) -> bool:
    try:
        import torch

        return isinstance(x, getattr(torch, "_subclasses").FakeTensor)
    except Exception:
        return False

