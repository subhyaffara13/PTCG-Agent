import re

def is_attr_private(attrname: str) -> Match[str] | None:
    """Check that attribute name is private (at least two leading underscores,
    at most one trailing underscore).
    """
    regex = re.compile("^_{2,10}.*[^_]+_?$")
    return regex.match(attrname)

