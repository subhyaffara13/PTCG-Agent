
def set_parent_type(state: StateBlock, name: str) -> Iterator[None]:
    """Temporarily set parent type to `name`"""
    oldParentType = state.parentType
    state.parentType = name
    yield
    state.parentType = oldParentType

