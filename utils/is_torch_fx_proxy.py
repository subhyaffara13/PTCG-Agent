
def is_torch_fx_proxy(x) -> bool:
    try:
        import torch.fx

        return isinstance(x, torch.fx.Proxy)
    except Exception:
        return False

