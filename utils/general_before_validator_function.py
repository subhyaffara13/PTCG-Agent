
def general_before_validator_function(*args, **kwargs):
    warnings.warn(
        '`general_before_validator_function` is deprecated, use `with_info_before_validator_function` instead.',
        DeprecationWarning,
    )
    return with_info_before_validator_function(*args, **kwargs)

