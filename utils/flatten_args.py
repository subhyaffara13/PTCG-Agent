
def flatten_args(args, *, detach: bool = False):
    """Flatten ``args`` into a list, optionally detaching tensors.

    Args:
        args: Nested arguments to flatten.
        detach: If ``True``, detach tensors while preserving ``requires_grad``.

    Returns:
        ``(new_args, flat_detached_args)`` when ``detach=True``;
        ``flat_args`` list otherwise.
    """
    flat_args, treespec = tree_flatten(args)

    if detach:
        flat_detached = [
            a.detach().requires_grad_(a.requires_grad)
            if isinstance(a, torch.Tensor)
            else a
            for a in flat_args
        ]
        new_args = tree_unflatten(flat_detached, treespec)
        return new_args, flat_detached

    return flat_args

