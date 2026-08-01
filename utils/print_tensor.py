
def print_tensor(
    path: OBJ_PATH,
    value: STATE_DICT_ITEM,
    print_fun: Callable[[str], None] = print,
) -> None:
    """
    Use this callback with traverse_state_dict to print its content.

    By default the content is printed using the builtin ``print`` but this can
    be change by passing a different ``print_fun` callable.
    """
    _print_nested(value, prefix=str(path), print_fun=print_fun)

