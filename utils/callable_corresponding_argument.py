
def callable_corresponding_argument(
    typ: NormalizedCallableType | Parameters, model: FormalArgument
) -> FormalArgument | None:
    """Return the argument of a function that corresponds to `model`"""

    by_name = typ.argument_by_name(model.name)
    by_pos = typ.argument_by_position(model.pos)
    if by_name is None and by_pos is None:
        return None
    if by_name is not None and by_pos is not None:
        if by_name == by_pos:
            return by_name
        # If we're dealing with an optional pos-only and an optional
        # name-only arg, merge them.  This is the case for all functions
        # taking both *args and **args, or a pair of functions like so:

        # def right(a: int = ...) -> None: ...
        # def left(x: int = ..., /, *, a: int = ...) -> None: ...
        from mypy.meet import meet_types

        if (
            not (by_name.required or by_pos.required)
            and by_pos.name is None
            and by_name.pos is None
            # This is not principled, but prevents a crash. It's weird to have a FormalArgument
            # that has an UnpackType.
            and not isinstance(by_name.typ, UnpackType)
            and not isinstance(by_pos.typ, UnpackType)
        ):
            return FormalArgument(
                by_name.name, by_pos.pos, meet_types(by_name.typ, by_pos.typ), False
            )
        return by_name

    return by_name if by_name is not None else by_pos

