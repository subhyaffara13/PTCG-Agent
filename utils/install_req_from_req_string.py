
def install_req_from_req_string(
    req_string: str,
    comes_from: InstallRequirement | None = None,
    isolated: bool = False,
    user_supplied: bool = False,
) -> InstallRequirement:
    try:
        req = get_requirement(req_string)
    except InvalidRequirement as exc:
        raise InstallationError(f"Invalid requirement: {req_string!r}: {exc}")

    domains_not_allowed = [
        PyPI.file_storage_domain,
        TestPyPI.file_storage_domain,
    ]
    if (
        req.url
        and comes_from
        and comes_from.link
        and comes_from.link.netloc in domains_not_allowed
    ):
        # Explicitly disallow pypi packages that depend on external urls
        raise InstallationError(
            "Packages installed from PyPI cannot depend on packages "
            "which are not also hosted on PyPI.\n"
            f"{comes_from.name} depends on {req} "
        )

    return InstallRequirement(
        req,
        comes_from,
        isolated=isolated,
        user_supplied=user_supplied,
    )

