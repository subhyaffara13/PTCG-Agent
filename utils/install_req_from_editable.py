
def install_req_from_editable(
    editable_req: str,
    comes_from: InstallRequirement | str | None = None,
    *,
    isolated: bool = False,
    hash_options: dict[str, list[str]] | None = None,
    constraint: bool = False,
    user_supplied: bool = False,
    permit_editable_wheels: bool = False,
    config_settings: dict[str, str | list[str]] | None = None,
) -> InstallRequirement:
    if constraint:
        raise InstallationError("Editable requirements are not allowed as constraints")

    parts = parse_req_from_editable(editable_req)
    return InstallRequirement(
        parts.requirement,
        comes_from=comes_from,
        user_supplied=user_supplied,
        editable=True,
        permit_editable_wheels=permit_editable_wheels,
        link=parts.link,
        constraint=constraint,
        isolated=isolated,
        hash_options=hash_options,
        config_settings=config_settings,
        extras=parts.extras,
    )

