
def parse_reqparts_from_editable(editable_req: str) -> RequirementParts:

    name, url, extras_override = parse_editable(editable_req)

    req = None
    if name is not None:
        try:
            req = Requirement(name)
        except InvalidRequirement as e:
            raise InstallationError(f"Invalid requirement: '{name}': {e}")

    return RequirementParts(
        requirement=req, 
        link=Link(url), 
        marker=None, 
        extras=extras_override,
    )

