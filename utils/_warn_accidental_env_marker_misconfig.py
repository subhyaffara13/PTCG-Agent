
def _warn_accidental_env_marker_misconfig(label: str, orig_value: str, parsed: list):
    """Because users sometimes misinterpret this configuration:

    [options.extras_require]
    foo = bar;python_version<"4"

    It looks like one requirement with an environment marker
    but because there is no newline, it's parsed as two requirements
    with a semicolon as separator.

    Therefore, if:
        * input string does not contain a newline AND
        * parsed result contains two requirements AND
        * parsing of the two parts from the result ("<first>;<second>")
        leads in a valid Requirement with a valid marker
    a UserWarning is shown to inform the user about the possible problem.
    """
    if "\n" in orig_value or len(parsed) != 2:
        return

    markers = marker_env().keys()

    try:
        req = Requirement(parsed[1])
        if req.name in markers:
            _AmbiguousMarker.emit(field=label, req=parsed[1])
    except InvalidRequirement as ex:
        if any(parsed[1].startswith(marker) for marker in markers):
            msg = _AmbiguousMarker.message(field=label, req=parsed[1])
            raise InvalidRequirement(msg) from ex

