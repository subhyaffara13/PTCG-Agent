
def literal_values(type_: type[Any]) -> tuple[Any, ...]:
    return get_args(type_)


def literal_values(type_: Type[Any]) -> Tuple[Any, ...]:
    return get_args(type_)

