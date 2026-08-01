
def is_list_type(typ: type) -> bool:
    return (get_origin(typ) or typ) == list

