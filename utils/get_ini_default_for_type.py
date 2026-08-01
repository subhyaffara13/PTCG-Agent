
def get_ini_default_for_type(
    type: Literal[
        "string", "paths", "pathlist", "args", "linelist", "bool", "int", "float"
    ],
) -> Any:
    """
    Used by addini to get the default value for a given config option type, when
    default is not supplied.
    """
    if type in ("paths", "pathlist", "args", "linelist"):
        return []
    elif type == "bool":
        return False
    elif type == "int":
        return 0
    elif type == "float":
        return 0.0
    else:
        return ""

