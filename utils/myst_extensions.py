
def myst_extensions(no_md=False):
    """The allowed extensions for the myst format."""
    if no_md:
        return [".myst", ".mystnb", ".mnb"]
    return [".md", ".myst", ".mystnb", ".mnb"]

