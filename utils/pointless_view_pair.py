
def pointless_view_pair(match: Match, arg, size1, size2):
    """
    Remove a pair of views that are pointless.
    """
    node = match.output_node()
    arg_size = list(arg.meta["val"].shape)
    if definitely_equal(arg_size, size2):
        node.replace_all_uses_with(arg)
        match.erase_nodes()
        counters["inductor"]["removed_pointless_view_pair"] += 1

