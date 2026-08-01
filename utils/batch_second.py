
def batch_second(args, kwargs):
    def set_batch_second(ew) -> None:
        ew.set_batch_first(False)

    def reset_batch_first(ew) -> None:
        ew.set_batch_first(True)

    tree_map_only(ExpandedWeight, set_batch_second, args)
    tree_map_only(ExpandedWeight, set_batch_second, kwargs)
    try:
        yield
    finally:
        tree_map_only(ExpandedWeight, reset_batch_first, args)
        tree_map_only(ExpandedWeight, reset_batch_first, kwargs)

