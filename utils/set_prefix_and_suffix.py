
def set_prefix_and_suffix(fmt, formats, nb_file):
    """Add prefix and suffix information from jupytext.formats if format and path matches"""
    for alt_fmt in long_form_multiple_formats(formats):
        if alt_fmt["extension"] == fmt["extension"] and fmt.get("format_name") == alt_fmt.get("format_name"):
            try:
                base_path(nb_file, alt_fmt)
                fmt.update(alt_fmt)
                return
            except InconsistentPath:
                continue

