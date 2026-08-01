
def parse_override_ini(override_ini: Sequence[str] | None) -> ConfigDict:
    """Parse the -o/--override-ini command line arguments and return the overrides.

    :raises UsageError:
        If one of the values is malformed.
    """
    overrides = {}
    # override_ini is a list of "ini=value" options.
    # Always use the last item if multiple values are set for same ini-name,
    # e.g. -o foo=bar1 -o foo=bar2 will set foo to bar2.
    for ini_config in override_ini or ():
        try:
            key, user_ini_value = ini_config.split("=", 1)
        except ValueError as e:
            raise UsageError(
                f"-o/--override-ini expects option=value style (got: {ini_config!r})."
            ) from e
        else:
            overrides[key] = ConfigValue(user_ini_value, origin="override", mode="ini")
    return overrides

