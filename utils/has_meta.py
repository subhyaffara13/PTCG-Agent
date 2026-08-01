
def has_meta(func: OpOverload) -> bool:
    return torch._C._dispatch_has_computed_kernel_for_dispatch_key(func.name(), "Meta")

