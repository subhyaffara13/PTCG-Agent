
def _unset_infra_mode(key):
    from torch._ops import _get_dispatch_mode_pre_dispatch, unset_mode_pre_dispatch

    pre_dispatch_mode = _get_dispatch_mode_pre_dispatch(key)
    post_dispatch_mode = torch._C._get_dispatch_mode(key)
    if pre_dispatch_mode and post_dispatch_mode:
        raise AssertionError(
            "Can't have active infra mode on both pre and post dispatch mode stack"
        )

    if pre_dispatch_mode:
        mode = unset_mode_pre_dispatch(key)
        return mode
    if post_dispatch_mode:
        return torch._C._unset_dispatch_mode(key)

