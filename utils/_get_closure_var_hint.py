
def _get_closure_var_hint(source: Source | None) -> str | None:
    """
    Walk up the source chain to find a CellContentsSource ancestor.
    Returns a hint like 'guard on "varname".attr' or None if not found.
    """
    if source is None:
        return None

    full_name = source.name
    current: Source | None = source
    while current is not None:
        if isinstance(current, CellContentsSource) and current.freevar_name:
            # Compute the path suffix by comparing names
            # e.g., full_name="x.__closure__[0].cell_contents.scale"
            #       current.name="x.__closure__[0].cell_contents"
            #       suffix=".scale"
            path_suffix = full_name[len(current.name) :]
            return f'guard on "{current.freevar_name}"{path_suffix}'
        current = current.base if isinstance(current, ChainedSource) else None
    return None

