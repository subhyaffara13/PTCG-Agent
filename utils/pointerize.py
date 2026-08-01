
def pointerize(decl: str, name: str) -> str:
    """Given a C decl and its name, modify it to be a declaration to a pointer."""
    # This doesn't work in general but does work for all our types...
    if "(" in decl:
        # Function pointer. Stick an * in front of the name and wrap it in parens.
        return decl.replace(name, f"(*{name})")
    else:
        # Non-function pointer. Just stick an * in front of the name.
        return decl.replace(name, f"*{name}")

