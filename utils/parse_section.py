
def parse_section(
    prefix: str,
    template: Options,
    set_strict_flags: Callable[[], None],
    section: Mapping[str, Any],
    config_types: dict[str, Any],
    stderr: TextIO = sys.stderr,
) -> tuple[dict[str, object], dict[str, str]]:
    """Parse one section of a config file.

    Returns a dict of option values encountered, and a dict of report directories.
    """
    results: dict[str, object] = {}
    report_dirs: dict[str, str] = {}

    # Because these fields exist on Options, without proactive checking, we would accept them
    # and crash later
    invalid_options = {
        "enabled_error_codes": "enable_error_code",
        "disabled_error_codes": "disable_error_code",
    }

    for key in section:
        invert = False
        # Here we use `key` for original config section key, and `options_key` for
        # the corresponding Options attribute.
        options_key = key
        # Match aliasing for deprecated config option name.
        if options_key == "allow_redefinition_new":
            options_key = "allow_redefinition"
        if key in config_types:
            ct = config_types[key]
        elif key in invalid_options:
            print(
                f"{prefix}Unrecognized option: {key} = {section[key]}"
                f" (did you mean {invalid_options[key]}?)",
                file=stderr,
            )
            continue
        else:
            dv = getattr(template, options_key, None)
            if dv is None:
                if key.endswith("_report"):
                    report_type = key[:-7].replace("_", "-")
                    if report_type in defaults.REPORTER_NAMES:
                        report_dirs[report_type] = str(section[key])
                    else:
                        print(f"{prefix}Unrecognized report type: {key}", file=stderr)
                    continue
                if key.startswith("x_"):
                    pass  # Don't complain about `x_blah` flags
                elif key.startswith("no_") and hasattr(template, options_key[3:]):
                    options_key = options_key[3:]
                    invert = True
                elif key.startswith("allow") and hasattr(template, "dis" + options_key):
                    options_key = "dis" + options_key
                    invert = True
                elif key.startswith("disallow") and hasattr(template, options_key[3:]):
                    options_key = options_key[3:]
                    invert = True
                elif key.startswith("show_") and hasattr(template, "hide_" + options_key[5:]):
                    options_key = "hide_" + options_key[5:]
                    invert = True
                elif key == "strict":
                    pass  # Special handling below
                else:
                    print(f"{prefix}Unrecognized option: {key} = {section[key]}", file=stderr)
                if invert:
                    dv = getattr(template, options_key, None)
                else:
                    continue
            ct = type(dv) if dv is not None else None
        v: Any = None
        try:
            if ct is bool:
                if isinstance(section, dict):
                    v = convert_to_boolean(section.get(key))
                else:
                    v = section.getboolean(key)  # type: ignore[attr-defined]  # Until better stub
                if invert:
                    v = not v
            elif callable(ct):
                if invert:
                    print(f"{prefix}Can not invert non-boolean key {options_key}", file=stderr)
                    continue
                try:
                    v = ct(section.get(key))
                except VersionTypeError as err_version:
                    print(f"{prefix}{key}: {err_version}", file=stderr)
                    v = err_version.fallback
                except argparse.ArgumentTypeError as err:
                    print(f"{prefix}{key}: {err}", file=stderr)
                    continue
            else:
                print(f"{prefix}Don't know what type {key} should have", file=stderr)
                continue
        except ValueError as err:
            print(f"{prefix}{key}: {err}", file=stderr)
            continue
        if key == "strict":
            if v:
                set_strict_flags()
            continue
        results[options_key] = v

    # These two flags act as per-module overrides, so store the empty defaults.
    if "disable_error_code" not in results:
        results["disable_error_code"] = []
    if "enable_error_code" not in results:
        results["enable_error_code"] = []

    return results, report_dirs

