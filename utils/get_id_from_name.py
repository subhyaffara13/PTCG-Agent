
def get_id_from_name(name: str, fullname: str, line: int) -> str:
    """Create a unique id for a function.

    This creates an id that is unique for any given function definition, so that it can be used as
    a dictionary key. This is usually the fullname of the function, but this is different in that
    it handles the case where the function is named '_', in which case multiple different functions
    could have the same name."""
    if unnamed_function(name):
        return f"{fullname}.{line}"
    else:
        return fullname

