
def has_user_subclass(args, allowed_subclasses):
    """Check if any tensor arguments are user subclasses.

    This is used to determine if tensor subclasses should get a chance to run
    their own implementation first before falling back to the default implementation.

    Args:
        args: Arguments to check (will be flattened with pytree)
        allowed_subclasses: Tuple of allowed subclass types

    Returns:
        True if user tensor subclasses are found, False otherwise
    """
    flat_args, _ = pytree.tree_flatten(args)

    val = any(
        isinstance(a, torch.Tensor)
        and type(a) is not torch.Tensor
        and not isinstance(a, allowed_subclasses)
        for a in flat_args
    )
    return val

