
def _get_non_persistent_buffers(mod: torch.nn.Module) -> set[str]:
    """
    Returns set of non-persistent buffers in a module and its submodules.
    """
    result: set[str] = set()
    for name, m in mod.named_modules(remove_duplicate=False):
        if name:
            result.update(f"{name}.{b}" for b in m._non_persistent_buffers_set)
        else:
            result.update(m._non_persistent_buffers_set)
    return result

