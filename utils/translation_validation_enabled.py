
def translation_validation_enabled() -> bool:
    # Checks every time this function is called, in case the Dynamo
    # option is set, but Z3 is not installed.
    _assert_z3_installed_if_tv_set()
    return _HAS_Z3 and config.translation_validation

