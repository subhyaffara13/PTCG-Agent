
def redact_auth_from_requirement(req: Requirement) -> str:
    """Replace the password in a given requirement url with ****."""
    if not req.url:
        return str(req)
    return str(req).replace(req.url, redact_auth_from_url(req.url))

