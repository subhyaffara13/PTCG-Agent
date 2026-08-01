
def _check_annotated_type(annotated_type: str, expected_type: str, annotation: str) -> None:
    if annotated_type != expected_type:
        raise PydanticUserError(f"'{annotation}' cannot annotate '{annotated_type}'.", code='invalid-annotated-type')

