
def _field_name_for_signature(field_name: str, field_info: FieldInfo) -> str:
    """Extract the correct name to use for the field when generating a signature.

    Assuming the field has a valid alias, this will return the alias. Otherwise, it will return the field name.
    First priority is given to the alias, then the validation_alias, then the field name.

    Args:
        field_name: The name of the field
        field_info: The corresponding FieldInfo object.

    Returns:
        The correct name to use when generating a signature.
    """
    if isinstance(field_info.alias, str) and is_valid_identifier(field_info.alias):
        return field_info.alias
    if isinstance(field_info.validation_alias, str) and is_valid_identifier(field_info.validation_alias):
        return field_info.validation_alias

    return field_name

