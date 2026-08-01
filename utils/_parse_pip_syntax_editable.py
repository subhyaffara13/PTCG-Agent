
def _parse_pip_syntax_editable(editable_req: str) -> tuple[str | None, str, set[str]]:
    url = editable_req

    # If a file path is specified with extras, strip off the extras.
    url_no_extras, extras = _strip_extras(url)

    if os.path.isdir(url_no_extras):
        # Treating it as code that has already been checked out
        url_no_extras = path_to_url(url_no_extras)

    if url_no_extras.lower().startswith("file:"):
        package_name = Link(url_no_extras).egg_fragment
        if extras:
            return (
                package_name,
                url_no_extras,
                get_requirement("placeholder" + extras.lower()).extras,
            )
        else:
            return package_name, url_no_extras, set()

    for version_control in vcs:
        if url.lower().startswith(f"{version_control}:"):
            url = f"{version_control}+{url}"
            break

    return Link(url).egg_fragment, url, set()

