
def to_graphable(stuff: pytree.PyTree) -> tuple[list[object], pytree.TreeSpec]:
    """Flattens stuff into a flat list of graphable types."""
    # We can consider preserving things like List[int] to improve
    # perf and readability (right now that is all flattened out)
    flat_args, spec = pytree.tree_flatten(stuff)
    for arg in flat_args:
        if not is_graphable(arg):
            raise RuntimeError(
                f"Expected all pytree.tree_leaves of (args, kwargs) to be graphable types, but found "
                f"non-fx-graphable type {type(arg)}. If this type is meant to be constant, mark it as "
                f"via pytree.register_constant; otherwise, register it as a pytree."
            )
    return flat_args, spec

