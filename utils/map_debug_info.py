
def map_debug_info(a: Argument) -> Argument:
    """
    Helper function to apply `friendly_debug_info` to items in `a`.
    `a` may be a list, tuple, or dict.
    """
    return torch.fx.node.map_aggregate(a, friendly_debug_info)

