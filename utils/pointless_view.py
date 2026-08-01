
def pointless_view(match: Match, arg, size):
    """Remove no-op view"""
    node = match.output_node()
    arg_size = list(node.args[0].meta["val"].shape)  # type: ignore[union-attr]
    if definitely_equal(arg_size, size):
        node.replace_all_uses_with(node.args[0])  # type: ignore[arg-type]
        match.erase_nodes()

