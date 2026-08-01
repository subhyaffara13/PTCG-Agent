
def format_name_for_ext(metadata, ext, cm_default_formats=None, explicit_default=True):
    """Return the format name for that extension"""
    # Is the format information available in the text representation?
    text_repr = metadata.get("jupytext", {}).get("text_representation", {})
    if text_repr.get("extension", "").endswith(ext) and text_repr.get("format_name"):
        return text_repr.get("format_name")

    # Format from jupytext.formats
    formats = metadata.get("jupytext", {}).get("formats", "") or cm_default_formats
    formats = long_form_multiple_formats(formats)
    for fmt in formats:
        if fmt["extension"] == ext:
            if (not explicit_default) or fmt.get("format_name"):
                return fmt.get("format_name")

    if (not explicit_default) or ext in [".md", ".markdown", ".Rmd"]:
        return None

    return get_format_implementation(ext).format_name

