
def _exception_type_name(
    e: type[BaseException] | tuple[type[BaseException], ...],
) -> str:
    if isinstance(e, type):
        return e.__name__
    if len(e) == 1:
        return e[0].__name__
    return "(" + ", ".join(ee.__name__ for ee in e) + ")"

