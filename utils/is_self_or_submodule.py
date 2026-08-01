
def is_self_or_submodule(name_descendant: str, name_ancestor: str) -> bool:
    """
    check if name_descendant is a submodule of name_ancestor, or if they are the same
    """
    return name_descendant == name_ancestor or name_ancestor + "." in name_descendant

