
def _parse_direct_url_editable(editable_req: str) -> tuple[str | None, str, set[str]]:
    try:
        req = Requirement(editable_req)
    except InvalidRequirement:
        pass
    else:
        if req.url:
            # Join the marker back into the name part. This will be parsed out
            # later into a Requirement again.
            if req.marker:
                name = f"{req.name} ; {req.marker}"
            else:
                name = req.name
            return (name, req.url, req.extras)

    raise ValueError

