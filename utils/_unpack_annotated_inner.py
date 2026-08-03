from typing import Any

def _unpack_annotated_inner(
    annotation: Any, unpack_type_aliases: Literal['lenient', 'eager'], check_annotated: bool
) -> tuple[Any, list[Any]]:
    origin = get_origin(annotation)
    if check_annotated and typing_objects.is_annotated(origin):
        annotated_type = annotation.__origin__
        metadata = list(annotation.__metadata__)

        # The annotated type might be a PEP 695 type alias, so we need to recursively
        # unpack it. Because Python already flattens `Annotated[Annotated[<type>, ...], ...]` forms,
        # we can skip the `is_annotated()` check in the next call:
        annotated_type, sub_meta = _unpack_annotated_inner(
            annotated_type, unpack_type_aliases=unpack_type_aliases, check_annotated=False
        )
        metadata = sub_meta + metadata
        return annotated_type, metadata
    elif typing_objects.is_typealiastype(annotation):
        try:
            value = annotation.__value__
        except NameError:
            if unpack_type_aliases == 'eager':
                raise
        else:
            typ, metadata = _unpack_annotated_inner(
                value, unpack_type_aliases=unpack_type_aliases, check_annotated=True
            )
            if metadata:
                # Having metadata means the type alias' `__value__` was an `Annotated` form
                # (or, recursively, a type alias to an `Annotated` form). It is important to check
                # for this, as we don't want to unpack other type aliases (e.g. `type MyInt = int`).
                return typ, metadata
            return annotation, []
    elif typing_objects.is_typealiastype(origin):
        # When parameterized, PEP 695 type aliases become generic aliases
        # (e.g. with `type MyList[T] = Annotated[list[T], ...]`, `MyList[int]`
        # is a generic alias).
        try:
            value = origin.__value__
        except NameError:
            if unpack_type_aliases == 'eager':
                raise
        else:
            # While Python already handles type variable replacement for simple `Annotated` forms,
            # we need to manually apply the same logic for PEP 695 type aliases:
            # - With `MyList = Annotated[list[T], ...]`, `MyList[int] == Annotated[list[int], ...]`
            # - With `type MyList[T] = Annotated[list[T], ...]`, `MyList[int].__value__ == Annotated[list[T], ...]`.

            try:
                # To do so, we emulate the parameterization of the value with the arguments:
                # with `type MyList[T] = Annotated[list[T], ...]`, to emulate `MyList[int]`,
                # we do `Annotated[list[T], ...][int]` (which gives `Annotated[list[T], ...]`):
                value = value[annotation.__args__]
            except TypeError:
                # Might happen if the type alias is parameterized, but its value doesn't have any
                # type variables, e.g. `type MyInt[T] = int`.
                pass
            typ, metadata = _unpack_annotated_inner(
                value, unpack_type_aliases=unpack_type_aliases, check_annotated=True
            )
            if metadata:
                return typ, metadata
            return annotation, []

    return annotation, []

