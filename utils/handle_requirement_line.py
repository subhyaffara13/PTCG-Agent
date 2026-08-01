
def handle_requirement_line(
    parsed_line: ParsedLine,
) -> ParsedRequirement:

    assert parsed_line.is_requirement

    if parsed_line.is_editable:
        # For editable requirements, we don't support per-requirement options,
        # so just return the parsed requirement: options are all invalid except
        # --editable of course
        invalid_options = get_options_by_dest(
            optparse_options=parsed_line.options,
            skip_editable=True,
        )

        return ParsedRequirement(
            requirement_string=parsed_line.requirement_string,
            is_editable=parsed_line.is_editable,
            is_constraint=parsed_line.is_constraint,
            requirement_line=parsed_line.requirement_line,
            invalid_options=invalid_options,
        )
    else:
        options = get_options_by_dest(
            optparse_options=parsed_line.options
        )

        # get the options that apply to requirements
        req_options = {}

        # these global options should not be on a requirement line
        invalid_options = {}

        for dest, value in options.items():
            if dest in SUPPORTED_OPTIONS_REQ_DEST:
                req_options[dest] = value
            else:
                invalid_options[dest] = value

        return ParsedRequirement(
            requirement_string=parsed_line.requirement_string,
            is_editable=parsed_line.is_editable,
            is_constraint=parsed_line.is_constraint,
            options=req_options,
            requirement_line=parsed_line.requirement_line,
            invalid_options=invalid_options,
        )


def handle_requirement_line(
    line: ParsedLine,
    options: optparse.Values | None = None,
) -> ParsedRequirement:
    # preserve for the nested code path
    line_comes_from = "{} {} (line {})".format(
        "-c" if line.constraint else "-r",
        line.filename,
        line.lineno,
    )

    assert line.requirement is not None

    # get the options that apply to requirements
    if line.is_editable:
        supported_dest = SUPPORTED_OPTIONS_EDITABLE_REQ_DEST
    else:
        supported_dest = SUPPORTED_OPTIONS_REQ_DEST
    req_options = {}
    for dest in supported_dest:
        if dest in line.opts.__dict__ and line.opts.__dict__[dest]:
            req_options[dest] = line.opts.__dict__[dest]

    line_source = f"line {line.lineno} of {line.filename}"
    return ParsedRequirement(
        requirement=line.requirement,
        is_editable=line.is_editable,
        comes_from=line_comes_from,
        constraint=line.constraint,
        options=req_options,
        line_source=line_source,
    )

