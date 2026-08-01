
def get_torch_dispatch_modes() -> list[TorchDispatchMode]:
    return torch.utils._python_dispatch._get_current_dispatch_mode_stack()

