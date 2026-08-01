
def read_metadata(text, ext):
    """Return the header metadata"""
    ext = "." + ext.split(".")[-1]
    lines = text.splitlines()

    if ext in [".md", ".markdown", ".Rmd"]:
        comment = comment_suffix = ""
    else:
        comment = _SCRIPT_EXTENSIONS.get(ext, {}).get("comment", "#")
        comment_suffix = _SCRIPT_EXTENSIONS.get(ext, {}).get("comment_suffix", "")

    metadata, _, _, _ = header_to_metadata_and_cell(lines, comment, comment_suffix, ext)
    if ext in [".r", ".R"] and not metadata:
        metadata, _, _, _ = header_to_metadata_and_cell(lines, "#'", "", ext)

    # metadata in MyST format may be at root level (i.e. not caught above)
    if not metadata and ext in myst_extensions() and text.startswith("---"):
        for header in yaml.safe_load_all(text):
            if not isinstance(header, dict):
                continue
            if header.get("jupytext", {}).get("text_representation", {}).get("format_name") == MYST_FORMAT_NAME:
                return header
            return metadata

    return metadata

