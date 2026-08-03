import re

def parse_type_ignore_tag(tag: str | None) -> list[str] | None:
    """Parse optional "[code, ...]" tag after "# type: ignore".

    Return:
     * [] if no tag was found (ignore all errors)
     * list of ignored error codes if a tag was found
     * None if the tag was invalid.
    """
    if not tag or tag.strip() == "" or tag.strip().startswith("#"):
        # No tag -- ignore all errors.
        return []
    m = re.match(r"\s*\[([^]#]*)\]\s*(#.*)?$", tag)
    if m is None:
        # Invalid "# type: ignore" comment.
        return None
    return [stripped_code for code in m.group(1).split(",") if (stripped_code := code.strip())]

