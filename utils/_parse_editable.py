import os

def _parse_editable(editable_req):
    url = editable_req

    # If a file path is specified with extras, strip off the extras.
    url_no_extras, extras = _strip_extras(url)
    original_url = url_no_extras

    if os.path.isdir(original_url):
        if not os.path.exists(os.path.join(original_url, "setup.py")):
            raise PipError(
                "Directory %r is not installable. File 'setup.py' not found."
                % original_url
            )
        # Treating it as code that has already been checked out
        url_no_extras = _path_to_url(url_no_extras)

    if url_no_extras.lower().startswith("file:"):
        # NOTE: url_no_extras may contain escaped characters here, meaning that
        # it may no longer be a literal package path. So we pass original_url.
        return _parse_local_package_name(original_url), url_no_extras

    if "+" not in url:
        raise PipError(
            "%s should either be a path to a local project or a VCS url "
            "beginning with svn+, git+, hg+, or bzr+" % editable_req
        )

    package_name = _egg_fragment(url)
    if not package_name:
        raise PipError(
            "Could not detect requirement name for '%s', please specify one "
            "with #egg=your_package_name" % editable_req
        )

    return package_name, url

