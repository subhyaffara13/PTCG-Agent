
def check_package_data(dist, attr, value):
    """Verify that value is a dictionary of package names to glob lists"""
    if not isinstance(value, dict):
        raise DistutilsSetupError(
            f"{attr!r} must be a dictionary mapping package names to lists of "
            "string wildcard patterns"
        )
    for k, v in value.items():
        if not isinstance(k, str):
            raise DistutilsSetupError(
                f"keys of {attr!r} dict must be strings (got {k!r})"
            )
        assert_string_list(dist, f'values of {attr!r} dict', v)

