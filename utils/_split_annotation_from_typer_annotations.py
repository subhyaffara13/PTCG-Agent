
def _split_annotation_from_typer_annotations(
    base_annotation: type[Any],
) -> tuple[type[Any], list[ParameterInfo]]:
    if get_origin(base_annotation) is not Annotated:
        return base_annotation, []
    base_annotation, *maybe_typer_annotations = get_args(base_annotation)
    return base_annotation, [
        annotation
        for annotation in maybe_typer_annotations
        if isinstance(annotation, ParameterInfo)
    ]

