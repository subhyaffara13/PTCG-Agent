
def do_striptags(value: "t.Union[str, HasHTML]") -> str:
    """Strip SGML/XML tags and replace adjacent whitespace by one space."""
    if hasattr(value, "__html__"):
        value = t.cast("HasHTML", value).__html__()

    return Markup(str(value)).striptags()

