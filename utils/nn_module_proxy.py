
def nn_module_proxy(mod: Any) -> Any:
    if not isinstance(mod, torch.nn.Module):
        return mod
    if isinstance(mod, torch.fx.GraphModule):
        # Dynamo-generated GM's shouldn't contain user-created GM's
        return mod
    proxy = mod.__class__.__new__(mod.__class__)
    proxy.__dict__ = mod.__dict__
    return proxy

