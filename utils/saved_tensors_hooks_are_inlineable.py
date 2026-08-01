
def saved_tensors_hooks_are_inlineable(hooks: Any) -> bool:
    if not hooks:
        return False
    pack, unpack = hooks
    return isinstance(pack, torch.fx.GraphModule) and isinstance(
        unpack, torch.fx.GraphModule
    )

