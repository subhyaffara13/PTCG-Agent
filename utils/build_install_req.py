
def build_install_req(
    requirement_string: str,
    requirement_line: Optional[RequirementLine] = None, # optional only for testing
    options: Optional[Dict[str, Any]] = None,
    invalid_options: Optional[Dict[str, Any]] = None,
    is_constraint: bool=False,
) -> InstallRequirement:
    """Create an InstallRequirement from a requirement_string, which might be a
    requirement, directory containing 'setup.py', filename, or URL.

    :param requirement_line: An optional RequirementLine describing where the
        line is from, for logging purposes in case of an error.
    """
    parts = parse_reqparts_from_string(requirement_string=requirement_string)

    return InstallRequirement(
        req=parts.requirement,
        requirement_line=requirement_line,
        link=parts.link,
        marker=parts.marker,
        install_options=options.get("install_options", []) if options else [],
        global_options=options.get("global_options", []) if options else [],
        hash_options=options.get("hashes", []) if options else [],
        is_constraint=is_constraint,
        extras=parts.extras,
        invalid_options=invalid_options or {},
    )

