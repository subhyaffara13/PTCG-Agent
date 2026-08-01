
def _register_node_impl(
    lib: torch.library.Library, node: _OverrideNode, dispatch_key: str
) -> None:
    """
    Register a single node implementation with the library.

    Args:
        lib: The torch.library.Library instance
        node: The override node to register
        dispatch_key: The dispatch key for registration
    """
    lib.impl(
        node.op_symbol,
        node.override_fn,
        dispatch_key,
        with_keyset=not node.unconditional_override,
        allow_override=True,
    )

