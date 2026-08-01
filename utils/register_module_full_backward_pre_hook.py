
def register_module_full_backward_pre_hook(
    hook: Callable[["Module", _grad_t], _grad_t | None],
) -> RemovableHandle:
    r"""Register a backward pre-hook common to all the modules.

    .. warning ::
        This adds global state to the `nn.module` module
        and it is only intended for debugging/profiling purposes.

    Hooks registered using this function behave in the same way as those
    registered by :meth:`torch.nn.Module.register_full_backward_pre_hook`.
    Refer to its documentation for more details.

    Hooks registered using this function will be called before hooks registered
    using :meth:`torch.nn.Module.register_full_backward_pre_hook`.

    Returns:
        :class:`torch.utils.hooks.RemovableHandle`:
            a handle that can be used to remove the added hook by calling
            ``handle.remove()``

    """
    handle = RemovableHandle(_global_backward_pre_hooks)
    _global_backward_pre_hooks[handle.id] = hook
    return handle

