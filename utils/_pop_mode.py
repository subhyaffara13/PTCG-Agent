
def _pop_mode():
    old = _pop_torch_function_stack()
    return old


def _pop_mode(k: DispatchKey | torch._C._TorchDispatchModeKey | None = None):
    if k == torch._C.DispatchKey.PreDispatch:  # type: ignore[attr-defined]
        from torch._ops import _pop_mode_from_pre_dispatch

        return _pop_mode_from_pre_dispatch()

    if k is None or isinstance(k, torch._C._TorchDispatchModeKey):
        return _pop_torch_dispatch_stack(k)

