
def get_element(
    root_dict: STATE_DICT_TYPE,
    path: OBJ_PATH,
    default_value: T | None = None,
) -> T | None:
    """Retrieve the value at ``path``from ``root_dict``, returning ``default_value`` if not found."""
    cur_value = cast(CONTAINER_TYPE, root_dict)
    for part in path:
        if type(part) is int:
            if not isinstance(cur_value, list) or len(cur_value) < part:
                return default_value
        elif not isinstance(cur_value, Mapping) or part not in cur_value:
            return default_value

        cur_value = cast(CONTAINER_TYPE, cur_value[part])
    return cast(T | None, cur_value)

