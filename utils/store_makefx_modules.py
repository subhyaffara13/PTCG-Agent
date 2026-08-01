
def store_makefx_modules(modules: list[torch.nn.Module]) -> tuple[int, ...]:
    """Store modules for the make_fx path and return their assigned indices.

    Uses negative indices to avoid collisions with Dynamo's register_user_object
    which uses non-negative indices.
    """
    global _makefx_next_index
    indices = []
    for mod in modules:
        _makefx_next_index -= 1
        _makefx_module_storage[_makefx_next_index] = mod
        indices.append(_makefx_next_index)
    return tuple(indices)

