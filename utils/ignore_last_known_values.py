
def ignore_last_known_values(t: UnionType) -> Type:
    """This will avoid types like str | str in error messages.

    last_known_values are kept during union simplification, but may cause
    weird formatting for e.g. tuples of literals.
    """
    union_items: list[Type] = []
    seen_instances = set()
    for item in t.items:
        if isinstance(item, ProperType) and isinstance(item, Instance):
            erased = item.copy_modified(last_known_value=None)
            if erased in seen_instances:
                continue
            seen_instances.add(erased)
            union_items.append(erased)
        else:
            union_items.append(item)
    return UnionType.make_union(union_items, t.line, t.column)

