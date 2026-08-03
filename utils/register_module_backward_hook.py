from typing import Callable

def register_module_backward_hook(
    hook: Callable[["Module", _grad_t, _grad_t], _grad_t | None],
) -> RemovableHandle:
    r"""Register a backward hook common to all the modules.

    This function is deprecated in favor of
    :func:`torch.nn.modules.module.register_module_full_backward_hook`
    and the behavior of this function will change in future versions.

    Returns:
        :class:`torch.utils.hooks.RemovableHandle`:
            a handle that can be used to remove the added hook by calling
            ``handle.remove()``

    """
    global _global_is_full_backward_hook
    if _global_is_full_backward_hook is True:
        raise RuntimeError(
            "Cannot use both regular backward hooks and full backward hooks as a "
            "global Module hook. Please use only one of them."
        )

    _global_is_full_backward_hook = False

    handle = RemovableHandle(_global_backward_hooks)
    _global_backward_hooks[handle.id] = hook
    return handle

