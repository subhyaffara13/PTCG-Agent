
def update_jupytext_formats_metadata(metadata, new_format):
    """Update the jupytext_format metadata in the Jupyter notebook"""
    new_format = long_form_one_format(new_format)
    formats = long_form_multiple_formats(metadata.get("jupytext", {}).get("formats", ""))
    if not formats:
        return

    for fmt in formats:
        if identical_format_path(fmt, new_format):
            fmt["format_name"] = new_format.get("format_name")
            break

    metadata.setdefault("jupytext", {})["formats"] = short_form_multiple_formats(formats)

