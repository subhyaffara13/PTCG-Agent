
def apply_validators(
    schema: core_schema.CoreSchema,
    validators: Iterable[Decorator[RootValidatorDecoratorInfo]]
    | Iterable[Decorator[ValidatorDecoratorInfo]]
    | Iterable[Decorator[FieldValidatorDecoratorInfo]],
) -> core_schema.CoreSchema:
    """Apply validators to a schema.

    Args:
        schema: The schema to apply validators on.
        validators: An iterable of validators.
        field_name: The name of the field if validators are being applied to a model field.

    Returns:
        The updated schema.
    """
    for validator in validators:
        # Actually, type could be 'field' or 'model', but this is only used for deprecated
        # decorators, so let's not worry about it.
        info_arg = inspect_validator(validator.func, mode=validator.info.mode, type='field')
        val_type = 'with-info' if info_arg else 'no-info'

        schema = _VALIDATOR_F_MATCH[(validator.info.mode, val_type)](validator.func, schema)
    return schema


def apply_validators(
    df: pd.DataFrame,
    fname: str,
    remediation: Remediation | None,
    validators: list[Validator],
    auto_accept: bool,
    write_out_file_func: Callable[..., Any],
) -> None:
    optional_remediations: list[Remediation] = []
    if remediation is not None:
        optional_remediations.append(remediation)
    for validator in validators:
        remediation = validator(df)
        if remediation is not None:
            optional_remediations.append(remediation)
            df = apply_necessary_remediation(df, remediation)

    any_optional_or_necessary_remediations = any(
        [
            remediation
            for remediation in optional_remediations
            if remediation.optional_msg is not None or remediation.necessary_msg is not None
        ]
    )
    any_necessary_applied = any(
        [remediation for remediation in optional_remediations if remediation.necessary_msg is not None]
    )
    any_optional_applied = False

    if any_optional_or_necessary_remediations:
        sys.stdout.write("\n\nBased on the analysis we will perform the following actions:\n")
        for remediation in optional_remediations:
            df, optional_applied = apply_optional_remediation(df, remediation, auto_accept)
            any_optional_applied = any_optional_applied or optional_applied
    else:
        sys.stdout.write("\n\nNo remediations found.\n")

    any_optional_or_necessary_applied = any_optional_applied or any_necessary_applied

    write_out_file_func(df, fname, any_optional_or_necessary_applied, auto_accept)

