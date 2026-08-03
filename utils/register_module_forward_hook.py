from typing import Callable

def register_module_forward_hook(
    hook: Callable[..., None],
    *,
    with_kwargs: bool = False,
    always_call: bool = False,
) -> RemovableHandle:
    r"""Register a global forward hook for all the modules.

    .. warning ::

        This adds global state to the `nn.module` module
        and it is only intended for debugging/profiling purposes.

    The hook will be called every time after :func:`forward` has computed an output.
    It should have the following signature::

        hook(module, input, output) -> None or modified output

    The input contains only the positional arguments given to the module.
    Keyword arguments won't be passed to the hooks and only to the ``forward``.
    You can optionally modify the output of the module by returning a new value
    that will replace the output from the :func:`forward` function.

    Parameters:
        hook (Callable): The user defined hook to be registered.
        always_call (bool): If ``True`` the ``hook`` will be run regardless of
            whether an exception is raised while calling the Module.
            Default: ``False``
    Returns:
        :class:`torch.utils.hooks.RemovableHandle`:
            a handle that can be used to remove the added hook by calling
            ``handle.remove()``

    This hook will be executed before specific module hooks registered with
    ``register_forward_hook``.
    """
    handle = RemovableHandle(
        _global_forward_hooks, extra_dict=_global_forward_hooks_always_called
    )
    _global_forward_hooks[handle.id] = hook
    if with_kwargs:
        _global_forward_hooks_with_kwargs[handle.id] = True
    if always_call:
        _global_forward_hooks_always_called[handle.id] = True
    return handle

