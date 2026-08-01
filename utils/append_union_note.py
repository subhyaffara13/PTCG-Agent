
def append_union_note(
    notes: list[str], arg_type: UnionType, expected_type: UnionType, options: Options
) -> list[str]:
    """Point to specific union item(s) that may cause failure in subtype check."""
    non_matching = []
    items = flatten_nested_unions(arg_type.items)
    if len(items) < MAX_UNION_ITEMS:
        return notes
    for item in items:
        if not is_subtype(item, expected_type):
            non_matching.append(item)
    if non_matching:
        types = ", ".join([format_type(typ, options) for typ in non_matching])
        notes.append(f"Item{plural_s(non_matching)} in the first union not in the second: {types}")
    return notes

