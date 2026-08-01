
def allow_smaller_batches(args, kwargs):
    def allow(ew) -> None:
        ew.set_allow_smaller_batches(True)

    def reset(ew) -> None:
        ew.set_allow_smaller_batches(False)

    tree_map_only(ExpandedWeight, allow, args)
    tree_map_only(ExpandedWeight, allow, kwargs)
    try:
        yield
    finally:
        tree_map_only(ExpandedWeight, reset, args)
        tree_map_only(ExpandedWeight, reset, kwargs)

