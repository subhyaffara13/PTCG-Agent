
def is_type_type_context(context: Type | None) -> bool:
    context = get_proper_type(context)
    if isinstance(context, TypeType):
        return True
    if isinstance(context, UnionType):
        return any(is_type_type_context(item) for item in context.items)
    return False

