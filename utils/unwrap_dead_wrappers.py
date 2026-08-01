
def unwrap_dead_wrappers(args: tuple[Any, ...]) -> tuple[Any, ...]:
    # NB: doesn't use tree_map_only for performance reasons
    result = tuple(
        unwrap_if_dead(arg) if isinstance(arg, torch.Tensor) else arg for arg in args
    )
    return result

