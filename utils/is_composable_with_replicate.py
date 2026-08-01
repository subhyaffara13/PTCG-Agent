
def is_composable_with_replicate(module: nn.Module) -> bool:
    registry = _get_registry(module)
    if registry is None:
        return True
    return "fully_shard" not in registry

