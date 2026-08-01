
def contains_type(type_hint, target_type) -> tuple[bool, object | None]:
    """
    Check if a "nested" type hint contains a specific target type,
    return the first-level type containing the target_type if found.
    """
    args = get_args(type_hint)
    if args == ():
        try:
            return issubclass(type_hint, target_type), type_hint
        except Exception:
            return issubclass(type(type_hint), target_type), type_hint
    found_type_tuple = [contains_type(arg, target_type)[0] for arg in args]
    found_type = any(found_type_tuple)
    if found_type:
        type_hint = args[found_type_tuple.index(True)]
    return found_type, type_hint

