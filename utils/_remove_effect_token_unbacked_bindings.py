
def _remove_effect_token_unbacked_bindings(
    node: torch.fx.Node,
) -> Generator[None, None, None]:
    """
    Temporarily modifies unbacked_bindings in a node's metadata by removing the first element
    of each path, which corresponds to an effect token.

    This is used when processing nodes that have effect tokens as the first element in their
    unbacked_bindings paths. The context manager ensures that the original bindings are
    restored after the operation is complete.

    Args:
        node: The FX node whose unbacked_bindings will be temporarily modified

    Yields:
        None
    """
    old_bindings = node.meta.get("unbacked_bindings", {})

    # Remove the extra layer for effect token
    new_bindings = {k: path[1:] if path else path for k, path in old_bindings.items()}

    node.meta["unbacked_bindings"] = new_bindings

    try:
        yield
    finally:
        node.meta["unbacked_bindings"] = old_bindings

