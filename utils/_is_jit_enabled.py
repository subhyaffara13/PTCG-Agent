
def _is_jit_enabled() -> "EnabledProxy":
    import torch.jit._state

    return torch.jit._state._enabled

