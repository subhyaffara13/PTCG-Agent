
def is_attr_protected(attrname: str) -> bool:
    """Return True if attribute name is protected (start with _ and some other
    details), False otherwise.
    """
    return (
        attrname[0] == "_"
        and attrname != "_"
        and not (attrname.startswith("__") and attrname.endswith("__"))
    )

