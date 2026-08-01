
def parse_req_from_editable(editable_req: str) -> RequirementParts:
    name, url, extras_override = parse_editable(editable_req)

    if name is not None:
        try:
            req: Requirement | None = get_requirement(name)
        except InvalidRequirement as exc:
            raise InstallationError(f"Invalid requirement: {name!r}: {exc}")
    else:
        req = None

    link = Link(url)

    return RequirementParts(req, link, None, extras_override)

