
def _push_mode(mode):
    _push_on_torch_function_stack(mode)


def _push_mode(mode: TorchDispatchMode) -> None:
    k = mode._dispatch_key if hasattr(mode, "_dispatch_key") else None
    if k is not None and k != torch._C.DispatchKey.PreDispatch:
        raise AssertionError(
            "mode._dispatch_key must be None or DispatchKey.PreDispatch"
        )
    if k is None:
        _push_on_torch_dispatch_stack(mode)
        return

    from torch._ops import _set_mode_pre_dispatch, get_cached_ops

    # See Note [Not Caching Per-Dispatch-Key Mode Handlers]
    # Clear the cache of every op that has been used so far, for this particular key.
    ks = torch._C._functionality_to_backend_keys(k)
    for op in get_cached_ops():
        for key in ks:
            op._uncache_dispatch(key)
    _set_mode_pre_dispatch(mode)

