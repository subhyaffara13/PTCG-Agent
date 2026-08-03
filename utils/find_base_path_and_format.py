import os

def find_base_path_and_format(main_path, formats: list[dict[str, str]]) -> tuple[str, dict[str, str]]:
    """Return the base path and the format corresponding to the given path"""
    for fmt in formats:
        try:
            return base_path(main_path, fmt), fmt
        except InconsistentPath:
            continue

    ext = os.path.splitext(main_path)[1][1:]
    raise InconsistentPath(
        f"Path '{main_path}' matches none of the export formats: {formats}. "
        f"Please make sure that jupytext.formats covers the current file "
        f"(e.g. add '{ext}' to the export formats)."
    )

