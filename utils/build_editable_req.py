
def build_editable_req(
    editable_req: str,
    requirement_line: Optional[RequirementLine] = None,  # optional for tests only
    options: Optional[Dict[str, Any]] = None,
    invalid_options: Optional[Dict[str, Any]] = None,
    is_constraint: bool = False,
) -> EditableRequirement:

    parts = parse_reqparts_from_editable(editable_req)

    return EditableRequirement(
        req=parts.requirement,
        requirement_line=requirement_line,
        link=parts.link,
        is_constraint=is_constraint,
        install_options=options.get("install_options", []) if options else [],
        global_options=options.get("global_options", []) if options else [],
        hash_options=options.get("hashes", []) if options else [],
        extras=parts.extras,
        invalid_options=invalid_options,
    )

