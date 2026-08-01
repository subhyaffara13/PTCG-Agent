
def exported_name(fullname: str) -> str:
    """Return a C name usable for an exported definition.

    This is like private_name(), but the output only depends on the
    'fullname' argument, so the names are distinct across multiple
    builds.
    """
    # TODO: Support unicode
    return fullname.replace("___", "___3_").replace(".", "___")

