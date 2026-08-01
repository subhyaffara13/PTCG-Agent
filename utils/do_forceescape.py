
def do_forceescape(value: "t.Union[str, HasHTML]") -> Markup:
    """Enforce HTML escaping.  This will probably double escape variables."""
    if hasattr(value, "__html__"):
        value = t.cast("HasHTML", value).__html__()

    return escape(str(value))

