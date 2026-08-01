
def collect_all_inner_types(t: Type) -> list[Type]:
    """
    Return all types that `t` contains
    """
    return t.accept(CollectAllInnerTypesQuery())

