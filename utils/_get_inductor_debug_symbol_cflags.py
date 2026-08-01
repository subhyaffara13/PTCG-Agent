
def _get_inductor_debug_symbol_cflags() -> tuple[list[str], list[str]]:
    """
    When we turn on generate debug symbol.
    On Windows, it should create a [module_name].pdb file. It helps debug by WinDBG.
    On Linux, it should create some debug sections in binary file.
    """
    cflags: list[str] = []
    ldflags: list[str] = []

    if _IS_WINDOWS:
        cflags = ["ZI", "_DEBUG"]
        ldflags = ["DEBUG", "ASSEMBLYDEBUG ", "OPT:REF", "OPT:ICF"]
    else:
        cflags.append("g")

    return cflags, ldflags

