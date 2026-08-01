
def _get_annotated_type(type_: type) -> type | None:
    """If the given type is an `Annotated` type then it is returned, if not `None` is returned.

    This also unwraps the type when applicable, e.g. `Required[Annotated[T, ...]]`
    """
    if is_required_type(type_):
        # Unwrap `Required[Annotated[T, ...]]` to `Annotated[T, ...]`
        type_ = get_args(type_)[0]

    if is_annotated_type(type_):
        return type_

    return None

