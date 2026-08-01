
def _ini_format(stream: TextIO, options: list[tuple[str, OptionDict, Any]]) -> None:
    """Format options using the INI format."""
    warnings.warn(
        "_ini_format has been deprecated. It will be removed in pylint 4.0.",
        DeprecationWarning,
        stacklevel=2,
    )
    for optname, optdict, value in options:
        # Skip deprecated option
        if "kwargs" in optdict:
            assert isinstance(optdict["kwargs"], dict)
            if "new_names" in optdict["kwargs"]:
                continue
        value = _format_option_value(optdict, value)
        help_opt = optdict.get("help")
        if help_opt:
            assert isinstance(help_opt, str)
            help_opt = normalize_text(help_opt, indent="# ")
            print(file=stream)
            print(help_opt, file=stream)
        else:
            print(file=stream)
        if value in {"None", "False"}:
            print(f"#{optname}=", file=stream)
        else:
            value = str(value).strip()
            if re.match(r"^([\w-]+,)+[\w-]+$", str(value)):
                separator = "\n " + " " * len(optname)
                value = separator.join(x + "," for x in str(value).split(","))
                # remove trailing ',' from last element of the list
                value = value[:-1]
            print(f"{optname}={value}", file=stream)

