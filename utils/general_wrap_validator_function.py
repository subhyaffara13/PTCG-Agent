
def general_wrap_validator_function(*args, **kwargs):
    warnings.warn(
        '`general_wrap_validator_function` is deprecated, use `with_info_wrap_validator_function` instead.',
        DeprecationWarning,
    )
    return with_info_wrap_validator_function(*args, **kwargs)

