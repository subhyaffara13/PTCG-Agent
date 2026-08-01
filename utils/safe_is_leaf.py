
def safe_is_leaf(t: MetaTensorDesc[Any] | torch.Tensor) -> bool:
    try:
        return t.is_leaf
    except RuntimeError:
        # inference mode can trigger this
        return False

