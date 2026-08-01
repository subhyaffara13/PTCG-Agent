
def _unpack_annotated(
    annotation: Any, /, *, unpack_type_aliases: Literal['skip', 'lenient', 'eager'] = 'eager'
) -> tuple[Any, list[Any]]:
    if unpack_type_aliases == 'skip':
        if typing_objects.is_annotated(get_origin(annotation)):
            return annotation.__origin__, list(annotation.__metadata__)
        else:
            return annotation, []

    return _unpack_annotated_inner(annotation, unpack_type_aliases=unpack_type_aliases, check_annotated=True)

