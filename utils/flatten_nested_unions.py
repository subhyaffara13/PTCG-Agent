
def flatten_nested_unions(
    types: Sequence[Type], *, handle_type_alias_type: bool = True, handle_recursive: bool = True
) -> list[Type]:
    """Flatten nested unions in a type list."""
    if not isinstance(types, list):
        typelist = list(types)
    else:
        typelist = cast("list[Type]", types)

    # Fast path: most of the time there is nothing to flatten
    if not any(isinstance(t, (TypeAliasType, UnionType)) for t in typelist):  # type: ignore[misc]
        return typelist

    flat_items: list[Type] = []
    for t in typelist:
        if handle_type_alias_type and isinstance(t, TypeAliasType):
            if not handle_recursive and t.is_recursive:
                tp: Type = t
            else:
                tp = get_proper_type(t)
        else:
            tp = t
        if isinstance(tp, ProperType) and isinstance(tp, UnionType):
            flat_items.extend(
                flatten_nested_unions(
                    tp.items,
                    handle_type_alias_type=handle_type_alias_type,
                    handle_recursive=handle_recursive,
                )
            )
        else:
            # Must preserve original aliases when possible.
            flat_items.append(t)
    return flat_items


def flatten_nested_unions(types: list[RType]) -> list[RType]:
    if not any(isinstance(t, RUnion) for t in types):
        return types  # Fast path

    flat_items: list[RType] = []
    for t in types:
        if isinstance(t, RUnion):
            flat_items.extend(flatten_nested_unions(t.items))
        else:
            flat_items.append(t)
    return flat_items

