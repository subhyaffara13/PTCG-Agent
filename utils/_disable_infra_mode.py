
def _disable_infra_mode(key):
    if key not in (
        torch._C._TorchDispatchModeKey.FUNCTIONAL,
        torch._C._TorchDispatchModeKey.PROXY,
    ):
        raise AssertionError(
            "key must be either FUNCTIONAL or PROXY _TorchDispatchModeKey"
        )
    mode_unset = _unset_infra_mode(key)
    try:
        yield mode_unset
    finally:
        if mode_unset is not None:
            _push_mode(mode_unset)

