
def has_overridden_vmap_rule(
    autograd_function: type[torch.autograd.Function],
) -> bool:
    return autograd_function.vmap is not torch.autograd.Function.vmap

