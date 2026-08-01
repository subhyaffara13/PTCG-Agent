
def shared_lib_name(group_name: str) -> str:
    """Given a group name, return the actual name of its extension module.

    (This just adds a suffix to the final component.)
    """
    return f"{group_name}__mypyc"

