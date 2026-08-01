
def _has_any_global_hook():
    return (
        _global_backward_pre_hooks
        or _global_backward_hooks
        or _global_forward_pre_hooks
        or _global_forward_hooks
        or _global_forward_hooks_always_called
        or _global_forward_hooks_with_kwargs
    )

