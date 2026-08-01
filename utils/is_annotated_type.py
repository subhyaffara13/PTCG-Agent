
def is_annotated_type(typ: type) -> bool:
    return get_origin(typ) == Annotated

