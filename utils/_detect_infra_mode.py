
def _detect_infra_mode(key):
    if key not in (
        torch._C._TorchDispatchModeKey.FUNCTIONAL,
        torch._C._TorchDispatchModeKey.PROXY,
    ):
        raise AssertionError(
            f"key must be either FUNCTIONAL ({torch._C._TorchDispatchModeKey.FUNCTIONAL}) \
                or PROXY ({torch._C._TorchDispatchModeKey.PROXY}) _TorchDispatchModeKey, \
                    got {key}"
        )
    from torch._ops import _get_dispatch_mode_pre_dispatch

    pre_dispatch_mode = _get_dispatch_mode_pre_dispatch(key)
    post_dispatch_mode = torch._C._get_dispatch_mode(key)

    if pre_dispatch_mode is not None and post_dispatch_mode is not None:
        raise AssertionError(
            "At most one of pre_dispatch_mode and post_dispatch_mode may be active"
        )

    if pre_dispatch_mode is None:
        return post_dispatch_mode

    return pre_dispatch_mode

