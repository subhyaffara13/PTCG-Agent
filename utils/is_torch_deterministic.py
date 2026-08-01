
def is_torch_deterministic() -> bool:
    """
    Check whether pytorch uses deterministic algorithms by looking if torch.set_deterministic_debug_mode() is set to 1 or 2"
    """
    if is_torch_available():
        import torch

        if torch.get_deterministic_debug_mode() == 0:
            return False
        else:
            return True

    return False

