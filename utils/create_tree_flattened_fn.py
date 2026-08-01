
def create_tree_flattened_fn(
    fn: Callable[..., Any],
    args: Sequence[Any],
    kwargs: dict[str, Any] | None = None,
) -> tuple[Callable[..., list[Any]], PytreeThunk]:
    if kwargs is None:
        kwargs = {}
    # Save the args_spec for flat_tensor_args to unflatten while tracing
    _, tensor_args_spec = pytree.tree_flatten((args, kwargs))
    out_spec = PytreeThunk()

    def flat_fn(*flat_args: Any) -> list[Any]:
        # The input are flattened tensor args. Prepare the args in the
        # order that original function expects. Add static args as well.
        # They will appear as tensor constants in the traced graph.
        nonlocal out_spec
        args, kwargs = pytree.tree_unflatten(flat_args, tensor_args_spec)
        tree_out = fn(*args, **kwargs)
        flat_out, spec = pytree.tree_flatten(tree_out)
        for i in flat_out:
            is_known_type = isinstance(i, tuple(KNOWN_TYPES)) or is_opaque_value(i)
            if not is_known_type:
                raise RuntimeError(
                    f"Found {type(i)} in output, which is not a known type. "
                    "If this type holds tensors, you need to register a pytree for it. "
                    "See https://github.com/pytorch/functorch/issues/475 for a brief "
                    "explanation why. If you don't need to register a pytree, please "
                    "leave a comment explaining your use case and we'll make this more "
                    "ergonomic to deal with"
                )
        out_spec.set(spec)
        return flat_out

    # Can't use functools.wraps here because the wrapper has different
    # calling convention
    if hasattr(fn, "_orig_mod"):
        # pyrefly: ignore[missing-attribute]
        flat_fn._orig_mod = fn._orig_mod

    return flat_fn, out_spec

