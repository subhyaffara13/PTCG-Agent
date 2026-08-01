
def _get_tag(_params: str) -> tuple[list[str], str]:
    """Separate the tag name from the admonition title."""
    params = _params.strip()
    if not params:
        return [""], ""

    with suppress(ValueError):
        return _get_multiple_tags(params)

    tag, *_title = params.split(" ")
    joined = " ".join(_title)

    title = ""
    if not joined:
        title = tag.title()
    elif joined != '""':  # Specifically check for no title
        title = joined
    return [tag.lower()], title

