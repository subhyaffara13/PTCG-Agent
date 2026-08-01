
def _get_tied_weight_keys(module: nn.Module) -> list[str]:
    tied_weight_keys: list[str] = []
    for name, submodule in module.named_modules():
        tied = getattr(submodule, "_tied_weights_keys", {}) or {}
        tied_weight_keys.extend([f"{name}.{k}" if name else k for k in tied.keys()])
    return tied_weight_keys

