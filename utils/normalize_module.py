from typing import Any

def normalize_module(
    root: torch.nn.Module,
    target: str,
    args: tuple[Any],
    kwargs: dict[str, Any] | None = None,
    normalize_to_only_use_kwargs: bool = False,
) -> ArgsKwargsPair | None:
    """
    Returns normalized arguments to PyTorch modules. This means that
    `args/kwargs` will be matched up to the functional's
    signature and return exclusively kwargs in positional order if
    `normalize_to_only_use_kwargs` is True.
    Also populates default values. Does not support positional-only
    parameters or varargs parameters (*args, **kwargs).

    Args:
        root (nn.Module): root module upon which we query modules
        target (Callable): Function that we are normalizing
        args (Tuple[Any]): Tuple of args to the function
        kwargs (Optional[Dict[str, Any]]): Dict of kwargs to the function
        normalize_to_only_use_kwargs (bool): Whether to normalize to only use kwargs.

    Returns:

        Returns normalized_args_and_kwargs, or `None` if not successful.
    """
    try:
        submod = root.get_submodule(target)
    except AttributeError as e:
        raise RuntimeError(
            f"Tried to normalize node with target {target} but root did not "
            f"have that target!"
        ) from e
    if hasattr(submod.__class__, "__name__"):
        classname = submod.__class__.__name__
        if getattr(torch.nn, classname, None) == submod.__class__:
            sig = inspect.signature(inspect.unwrap(submod.forward))
            if kwargs is None:
                kwargs = {}
            new_args_and_kwargs = _args_kwargs_to_normalized_args_kwargs(
                sig, args, kwargs, normalize_to_only_use_kwargs
            )
            return new_args_and_kwargs
    return None

