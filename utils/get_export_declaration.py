
def get_export_declaration():
    return "__declspec(dllexport)" if _IS_WINDOWS else ""

