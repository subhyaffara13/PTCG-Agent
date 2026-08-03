import os
import re

def _parse_requirement_url(req_str):
    original_req_str = req_str

    # Some requirements lines begin with a `git+` or similar to indicate the VCS. If this is the
    # case, remove this before proceeding any further.
    for v in VCS_SCHEMES:
        if req_str.startswith(v + "+"):
            req_str = req_str[len(v) + 1 :]
            break

    # Strip out the marker temporarily while we parse out any potential URLs
    marker_sep = "; " if _is_url(req_str) else ";"
    marker_str = None
    link = None
    if ";" in req_str:
        req_str, marker_str = req_str.split(marker_sep, 1)

    if _is_url(req_str):
        link = Link(req_str)
    else:
        path = os.path.normpath(os.path.abspath(req_str))
        p, _ = _strip_extras(path)
        url = _get_url_from_path(p, req_str)
        if url is not None:
            link = Link(url)

    # it's a local file, dir, or url
    if link is not None:
        # Handle relative file URLs
        if link.scheme == "file" and re.search(r"\.\./", link.url):
            link = Link(_path_to_url(os.path.normpath(os.path.abspath(link.path))))
        # wheel file
        if link.is_wheel:
            wheel_info = WHEEL_FILE_RE.match(link.filename)
            if wheel_info is None:
                raise PipError(f"Invalid wheel name: {link.filename}")
            wheel_name = wheel_info.group("name").replace("_", "-")
            wheel_version = wheel_info.group("ver").replace("_", "-")
            req_str = f"{wheel_name}=={wheel_version}"
        else:
            # set the req to the egg fragment.  when it's not there, this
            # will become an 'unnamed' requirement
            req_str = _egg_fragment(link.url)
            if req_str is None:
                raise PipError(f"Missing egg fragment in URL: {original_req_str}")
            req_str = f"{req_str}@{link.url}"

    # Reassemble the requirement string with the original marker
    if marker_str is not None:
        req_str = f"{req_str}{marker_sep}{marker_str}"

    return req_str

