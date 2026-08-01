
def field_plain_validator_function(function: WithInfoValidatorFunction, field_name: str, **kwargs):
    warnings.warn(
        '`field_plain_validator_function` is deprecated, use `with_info_plain_validator_function` instead.',
        DeprecationWarning,
    )
    return with_info_plain_validator_function(function, field_name=field_name, **kwargs)

