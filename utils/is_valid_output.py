
def is_valid_output(x: tuple[object, ...]) -> TypeIs[tuple[_FXOutput, ...]]: ...


def is_valid_output(x: Sequence[object]) -> TypeIs[Sequence[_FXOutput]]: ...


def is_valid_output(x: object) -> bool:
    if isinstance(x, (tuple, list)):
        return all(map(is_valid_output, x))
    return is_graphable(x)

