
def _validate_pre(pre: object, /) -> TypeGuard[bool | None]:
    return pre is None or isinstance(pre, bool)


def _validate_pre(value: object, /) -> tuple[Literal["a", "b", "rc"], int] | None:
    if value is None:
        return value
    if isinstance(value, tuple) and len(value) == 2:
        letter, number = value
        letter = normalize_pre(letter)
        if letter in {"a", "b", "rc"} and isinstance(number, int) and number >= 0:
            # type checkers can't infer the Literal type here on letter
            return (letter, number)  # type: ignore[return-value]
    msg = f"pre must be a tuple of ('a'|'b'|'rc', non-negative int), got {value}"
    raise InvalidVersion(msg)


def _validate_pre(value: object, /) -> tuple[Literal["a", "b", "rc"], int] | None:
    if value is None:
        return value
    if (
        isinstance(value, tuple)
        and len(value) == 2
        and value[0] in ("a", "b", "rc")
        and isinstance(value[1], int)
        and value[1] >= 0
    ):
        return value
    msg = f"pre must be a tuple of ('a'|'b'|'rc', non-negative int), got {value}"
    raise InvalidVersion(msg)


def _validate_pre(pre: object, /) -> TypeGuard[bool | None]:
    return pre is None or isinstance(pre, bool)


def _validate_pre(value: object, /) -> tuple[Literal["a", "b", "rc"], int] | None:
    if value is None:
        return value
    if isinstance(value, tuple) and len(value) == 2:
        letter, number = value
        letter = normalize_pre(letter)
        if letter in {"a", "b", "rc"} and isinstance(number, int) and number >= 0:
            # type checkers can't infer the Literal type here on letter
            return (letter, number)  # type: ignore[return-value]
    msg = f"pre must be a tuple of ('a'|'b'|'rc', non-negative int), got {value}"
    raise InvalidVersion(msg)

