
def field_before_validator_function(function: WithInfoValidatorFunction, field_name: str, schema: CoreSchema, **kwargs):
    warnings.warn(
        '`field_before_validator_function` is deprecated, use `with_info_before_validator_function` instead.',
        DeprecationWarning,
    )
    return with_info_before_validator_function(function, schema, field_name=field_name, **kwargs)

