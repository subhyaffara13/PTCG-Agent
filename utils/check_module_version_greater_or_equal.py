
def check_module_version_greater_or_equal(
    module,
    req_version_tuple,
    error_if_malformed=True,
):
    """
    Check if a module's version satisfies requirements

    Usually, a module's version string will be like 'x.y.z', which would be represented
    as a tuple (x, y, z), but sometimes it could be an unexpected format. If the version
    string does not match the given tuple's format up to the length of the tuple, then
    error and exit or emit a warning.

    Args:
        module: the module to check the version of
        req_version_tuple: tuple (usually of ints) representing the required version
        error_if_malformed: whether we should exit if module version string is malformed

    Returns:
        requirement_is_met: bool
    """
    try:
        version_strs = module.__version__.split(".")
        # Cast module version fields to match the types of the required version
        module_version = tuple(
            type(req_field)(version_strs[idx])
            for idx, req_field in enumerate(req_version_tuple)
        )
        requirement_is_met = module_version >= req_version_tuple

    except Exception as e:
        message = (
            f"'{module.__name__}' module version string is malformed '{module.__version__}' and cannot be compared"
            f" with tuple {str(req_version_tuple)}"
        )
        if error_if_malformed:
            raise RuntimeError(message) from e
        else:
            warnings.warn(
                message + ", but continuing assuming that requirement is met",
                stacklevel=2,
            )
            requirement_is_met = True

    return requirement_is_met

