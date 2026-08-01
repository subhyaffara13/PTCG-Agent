
def get_bad_type_type_item(item: Type) -> str | None:
    """Prohibit types like Type[Type[...]].

    Such types are explicitly prohibited by PEP 484. Also, they cause problems
    with recursive types like T = Type[T], because internal representation of
    TypeType item is normalized (i.e. always a proper type).

    Also forbids `Type[Literal[...]]`, because typing spec does not allow it.
    """
    # TODO: what else cannot be present in `type[...]`?
    item = get_proper_type(item)
    if isinstance(item, TypeType):
        return "Type[...]"
    if isinstance(item, LiteralType):
        return "Literal[...]"
    if isinstance(item, UnionType):
        items = [
            bad_item
            for typ in flatten_nested_unions(item.items)
            if (bad_item := get_bad_type_type_item(typ)) is not None
        ]
        if not items:
            return None
        if len(items) == 1:
            return items[0]
        return f"Union[{', '.join(items)}]"
    return None

