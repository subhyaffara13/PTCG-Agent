
def install_req_from_parsed_requirement(
    parsed_req: ParsedRequirement,
    isolated: bool = False,
    user_supplied: bool = False,
    config_settings: dict[str, str | list[str]] | None = None,
) -> InstallRequirement:
    if parsed_req.is_editable:
        req = install_req_from_editable(
            parsed_req.requirement,
            comes_from=parsed_req.comes_from,
            constraint=parsed_req.constraint,
            isolated=isolated,
            user_supplied=user_supplied,
            config_settings=config_settings,
        )

    else:
        req = install_req_from_line(
            parsed_req.requirement,
            comes_from=parsed_req.comes_from,
            isolated=isolated,
            hash_options=(
                parsed_req.options.get("hashes", {}) if parsed_req.options else {}
            ),
            constraint=parsed_req.constraint,
            line_source=parsed_req.line_source,
            user_supplied=user_supplied,
            config_settings=config_settings,
        )
    return req

