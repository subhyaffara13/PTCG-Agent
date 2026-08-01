
def install_req_from_line(
    name: str,
    comes_from: str | InstallRequirement | None = None,
    *,
    isolated: bool = False,
    hash_options: dict[str, list[str]] | None = None,
    constraint: bool = False,
    line_source: str | None = None,
    user_supplied: bool = False,
    config_settings: dict[str, str | list[str]] | None = None,
) -> InstallRequirement:
    """Creates an InstallRequirement from a name, which might be a
    requirement, directory containing 'setup.py', filename, or URL.

    :param line_source: An optional string describing where the line is from,
        for logging purposes in case of an error.
    """
    parts = parse_req_from_line(name, line_source)

    return InstallRequirement(
        parts.requirement,
        comes_from,
        link=parts.link,
        markers=parts.markers,
        isolated=isolated,
        hash_options=hash_options,
        config_settings=config_settings,
        constraint=constraint,
        extras=parts.extras,
        user_supplied=user_supplied,
    )

