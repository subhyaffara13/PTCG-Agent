
def _get_extended_precision_list() -> list[str]:
    extended_names = [
        "float96",
        "float128",
        "complex192",
        "complex256",
    ]
    return [i for i in extended_names if hasattr(np, i)]

