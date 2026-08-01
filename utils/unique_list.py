
def unique_list(l):
    """ Uniquify a list (skip duplicate items). """
    result = []
    for x in l:
        if x not in result:
            result.append(x)
    return result


def unique_list(
    input_list: Union[List[T], Tuple[T, ...]],
    *,
    name_factory: Callable[[T], str] = str,
) -> List[T]:
    """
    Make a list unique while maintaining order.
    We update the list if another one with the same name is set
    (e.g. root validator overridden in subclass)
    """
    result: List[T] = []
    result_names: List[str] = []
    for v in input_list:
        v_name = name_factory(v)
        if v_name not in result_names:
            result_names.append(v_name)
            result.append(v)
        else:
            result[result_names.index(v_name)] = v

    return result


def unique_list(
    input_list: list[T] | tuple[T, ...],
    *,
    name_factory: Callable[[T], str] = str,
) -> list[T]:
    """Make a list unique while maintaining order.
    We update the list if another one with the same name is set
    (e.g. model validator overridden in subclass).
    """
    result: list[T] = []
    result_names: list[str] = []
    for v in input_list:
        v_name = name_factory(v)
        if v_name not in result_names:
            result_names.append(v_name)
            result.append(v)
        else:
            result[result_names.index(v_name)] = v

    return result

