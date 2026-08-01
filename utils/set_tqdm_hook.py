
def set_tqdm_hook(hook: Callable[[Callable[..., Any], tuple[Any, ...], dict[str, Any]], Any] | None):
    """
    Set a hook that customizes tqdm creation.

    The hook is called with the tqdm factory to use (either `tqdm.auto.tqdm` or an empty shim), along with the
    positional and keyword arguments that would have been passed to tqdm. The hook should return an object compatible
    with tqdm (i.e. implementing the methods your code relies on, such as `update`, `close`, context manager methods,
    etc.).

    Passing `None` clears the hook.

    Returns:
        The previous hook, which can be restored later.
    """
    global _tqdm_hook
    previous_hook = _tqdm_hook
    _tqdm_hook = hook
    return previous_hook

