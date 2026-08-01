
def build_req_from_parsedreq(
    parsed_req: ParsedRequirement,
) -> InstallRequirement:

    requirement_string = parsed_req.requirement_string
    options = parsed_req.options
    invalid_options = parsed_req.invalid_options
    requirement_line = parsed_req.requirement_line
    is_constraint = parsed_req.is_constraint

    if parsed_req.is_editable:
        return build_editable_req(
            editable_req=requirement_string,
            requirement_line=requirement_line,
            options=options,
            is_constraint=is_constraint,
            invalid_options=invalid_options,
        )

    return build_install_req(
        requirement_string=requirement_string,
        requirement_line=requirement_line,
        options=options,
        is_constraint=is_constraint,
        invalid_options=invalid_options,
    )

