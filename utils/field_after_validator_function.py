
def field_after_validator_function(function: WithInfoValidatorFunction, field_name: str, schema: CoreSchema, **kwargs):
    warnings.warn(
        '`field_after_validator_function` is deprecated, use `with_info_after_validator_function` instead.',
        DeprecationWarning,
    )
    return with_info_after_validator_function(function, schema, field_name=field_name, **kwargs)

