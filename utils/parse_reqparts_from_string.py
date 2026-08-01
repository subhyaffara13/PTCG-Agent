
def parse_reqparts_from_string(requirement_string: str) -> RequirementParts:
    """
    Return RequirementParts from a ``requirement_string``.
    Raise exceptions on error.
    """
    if is_url(requirement_string):
        marker_sep = "; "
    else:
        marker_sep = ";"

    if marker_sep in requirement_string:
        requirement_string, marker_as_string = requirement_string.split(marker_sep, 1)
        marker_as_string = marker_as_string.strip()
        if not marker_as_string:
            marker = None
        else:
            marker = Marker(marker_as_string)
    else:
        marker = None
    requirement_string_no_marker = requirement_string.strip()

    req_as_string = None
    path = requirement_string_no_marker
    link = None
    extras_as_string = None

    if is_url(requirement_string_no_marker):
        link = Link(requirement_string_no_marker)
    elif not is_name_at_url_requirement(requirement_string_no_marker):
        p, extras_as_string = _strip_extras(path)
        url = _get_url_from_path(p, requirement_string_no_marker)
        if url:
            link = Link(url)

    # it's a local file, dir, or url
    if link:
        # Handle relative file URLs
        if link.scheme == "file" and re.search(r"\.\./", link.url):
            link = Link(link.path)
        # wheel file
        if link.is_wheel:
            wheel = Wheel(link.filename)  # can raise InvalidWheelFilename
            req_as_string = f"{wheel.name}=={wheel.version}"
        else:
            # set the req to the egg fragment.  when it's not there, this
            # will become an 'unnamed' requirement
            req_as_string = link.egg_fragment

    # a requirement specifier that should be packaging-parsable.
    # this includes name@url
    else:
        req_as_string = requirement_string_no_marker

    extras = convert_extras(extras_as_string)

    def _parse_req_string(req_as_string: str) -> Requirement:
        rq = None
        try:
            rq = Requirement(req_as_string)
        except InvalidRequirement as e:
            if os.path.sep in req_as_string:
                add_msg = "It looks like a path."

            elif "=" in req_as_string and not any(
                op in req_as_string for op in operators
            ):
                add_msg = "= is not a valid operator. Did you mean == ?"

            else:
                add_msg = ""
            msg = f"Invalid requirement: {add_msg}: {e}"
            raise InstallationError(msg)
        else:
            # Deprecate extras after specifiers: "name>=1.0[extras]"
            # This currently works by accident because _strip_extras() parses
            # any extras in the end of the string and those are saved in
            # RequirementParts
            for spec in rq.specifier:
                spec_str = str(spec)
                if spec_str.endswith("]"):
                    msg = f"Unsupported extras after version '{spec_str}'."
                    raise InstallationError(msg)
        return rq

    if req_as_string is not None:
        req: Optional[Requirement] = _parse_req_string(req_as_string)
    else:
        req = None

    return RequirementParts(req, link, marker, extras)

