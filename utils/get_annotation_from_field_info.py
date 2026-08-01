
def get_annotation_from_field_info(
    annotation: Any, field_info: FieldInfo, field_name: str, validate_assignment: bool = False
) -> Type[Any]:
    """
    Get an annotation with validation implemented for numbers and strings based on the field_info.
    :param annotation: an annotation from a field specification, as ``str``, ``ConstrainedStr``
    :param field_info: an instance of FieldInfo, possibly with declarations for validations and JSON Schema
    :param field_name: name of the field for use in error messages
    :param validate_assignment: default False, flag for BaseModel Config value of validate_assignment
    :return: the same ``annotation`` if unmodified or a new annotation with validation in place
    """
    constraints = field_info.get_constraints()
    used_constraints: Set[str] = set()
    if constraints:
        annotation, used_constraints = get_annotation_with_constraints(annotation, field_info)
    if validate_assignment:
        used_constraints.add('allow_mutation')

    unused_constraints = constraints - used_constraints
    if unused_constraints:
        raise ValueError(
            f'On field "{field_name}" the following field constraints are set but not enforced: '
            f'{", ".join(unused_constraints)}. '
            f'\nFor more details see https://docs.pydantic.dev/usage/schema/#unenforced-field-constraints'
        )

    return annotation

