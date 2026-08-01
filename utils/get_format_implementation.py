
def get_format_implementation(ext, format_name=None):
    """Return the implementation for the desired format"""
    # remove pre-extension if any
    ext = "." + ext.split(".")[-1]

    formats_for_extension = []
    for fmt in JUPYTEXT_FORMATS:
        if fmt.extension == ext:
            if fmt.format_name == format_name or not format_name:
                return fmt
            formats_for_extension.append(fmt.format_name)

    if formats_for_extension:
        raise JupytextFormatError(
            "Format '{}' is not associated to extension '{}'. Please choose one of: {}.".format(
                format_name, ext, ", ".join(formats_for_extension)
            )
        )
    raise JupytextFormatError(f"No format associated to extension '{ext}'")

