from typing import Optional, Set, Tuple

def parse_editable(editable_req: str) -> Tuple[Optional[str], str, Set[str]]:
    """Parses an editable requirement into:
        - a requirement name
        - an URL
        - extras

    Accepted requirements:
        svn+http://blahblah@rev#egg=Foobar[baz]
        .[some_extra]
    """

    url = editable_req

    # If a file path is specified with extras, strip off the extras.
    url_no_extras, extras = _strip_extras(url)

    unel = url_no_extras.lower()
    if (
        unel.startswith(("file:", ".",))
        or _looks_like_path(unel)
        or _is_plain_name(unel)
    ):
        package_name = Link(url_no_extras).egg_fragment
        if extras:
            return (
                package_name,
                url_no_extras,
                Requirement("placeholder" + extras.lower()).extras,
            )
        else:
            return package_name, url_no_extras, set()

    for version_control in vcs:
        if url.lower().startswith(f"{version_control}:"):
            url = f"{version_control}+{url}"
            break

    link = Link(url)

    is_path_like = _looks_like_path(url) or _is_plain_name(url)

    if not (link.is_vcs or is_path_like):
        backends = ", ".join(vcs_all_schemes)
        raise InstallationError(
            f"{editable_req} is not a valid editable requirement. "
            f"It should either be a path to a local project or a VCS URL "
            f"(beginning with {backends})."
        )

    package_name = link.egg_fragment
    if not package_name and not is_path_like:
        raise InstallationError(
            "Could not detect requirement name for '{}', please specify one "
            "with #egg=your_package_name".format(editable_req)
        )
    return package_name, url, set()


def parse_editable(editable_req: str) -> tuple[str | None, str, set[str]]:
    """Parses an editable requirement into:
        - a requirement name with environment markers
        - an URL
        - extras
    Accepted requirements:
        - svn+http://blahblah@rev#egg=Foobar[baz]&subdirectory=version_subdir
        - local_path[some_extra]
        - Foobar[extra] @ svn+http://blahblah@rev#subdirectory=subdir ; markers
    """
    try:
        package_name, url, extras = _parse_direct_url_editable(editable_req)
    except ValueError:
        package_name, url, extras = _parse_pip_syntax_editable(editable_req)

    link = Link(url)

    if not link.is_vcs and not link.url.startswith("file:"):
        backends = ", ".join(vcs.all_schemes)
        raise InstallationError(
            f"{editable_req} is not a valid editable requirement. "
            f"It should either be a path to a local project or a VCS URL "
            f"(beginning with {backends})."
        )

    # The project name can be inferred from local file URIs easily.
    if not package_name and not link.url.startswith("file:"):
        raise InstallationError(
            f"Could not detect requirement name for '{editable_req}', "
            "please specify one with your_package_name @ URL"
        )
    return package_name, url, extras

