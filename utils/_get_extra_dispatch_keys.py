
def _get_extra_dispatch_keys(t: torch.Tensor) -> DispatchKeySet:
    extra_dispatch_keys = torch._C.DispatchKeySet.from_raw_repr(0)
    if torch._C._dispatch_keys(t).has(torch._C.DispatchKey.Conjugate):
        extra_dispatch_keys = extra_dispatch_keys.add(torch._C.DispatchKey.Conjugate)
    if torch._C._dispatch_keys(t).has(torch._C.DispatchKey.Negative):
        extra_dispatch_keys = extra_dispatch_keys.add(torch._C.DispatchKey.Negative)
    return extra_dispatch_keys

