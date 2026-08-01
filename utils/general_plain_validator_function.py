
def general_plain_validator_function(*args, **kwargs):
    warnings.warn(
        '`general_plain_validator_function` is deprecated, use `with_info_plain_validator_function` instead.',
        DeprecationWarning,
    )
    return with_info_plain_validator_function(*args, **kwargs)

