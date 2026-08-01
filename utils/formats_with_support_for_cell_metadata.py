
def formats_with_support_for_cell_metadata():
    for fmt in JUPYTEXT_FORMATS:
        if fmt.format_name == "myst" and not is_myst_available():
            continue
        if fmt.format_name == "pandoc" and not is_pandoc_available():
            continue
        if fmt.format_name in FORMATS_WITH_NO_CELL_METADATA:
            continue

        yield f"{fmt.extension[1:]}:{fmt.format_name}"

