
def read_format_from_metadata(text, ext):
    """Return the format of the file, when that information is available from the metadata"""
    metadata = read_metadata(text, ext)
    rearrange_jupytext_metadata(metadata)
    return format_name_for_ext(metadata, ext, explicit_default=False)

