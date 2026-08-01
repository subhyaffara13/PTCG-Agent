
def dumps_global_options(options):
    """
    Given a mapping of options, return a string suitable for use in a pip
    requirements file. Raise Exception if the options name or value type is
    unknown.
    """
    option_items = []

    for name, value in sorted(options.items()):
        opt_string = OPT_BY_OPTIONS_DEST.get(name)

        invalid_message = (
            f"Internal error: Unknown requirement option {name!r} "
            f"with value: {value!r}"
        )

        if not opt_string:
            raise InstallationError(invalid_message)

        if isinstance(value, list):
            for val in value:
                option_items.append(f"{opt_string} {val}")

        elif isinstance(value, str):
            option_items.append(f"{opt_string} {value}")

        elif isinstance(value, bool) or value is None:
            option_items.append(f"{opt_string}")

        else:
            raise InstallationError(invalid_message)

    return " ".join(option_items)

