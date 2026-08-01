
def _is_fully_sharded(module: nn.Module) -> bool:
    r"""Check if module is marked with fully_shard."""
    registry = _get_registry(module)
    if registry is None:
        return False
    return "fully_shard" in registry

