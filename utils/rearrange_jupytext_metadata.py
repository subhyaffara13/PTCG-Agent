
def rearrange_jupytext_metadata(metadata):
    """Convert the jupytext_formats metadata entry to jupytext/formats, etc. See #91"""

    # Backward compatibility with nbrmd
    for key in ["nbrmd_formats", "nbrmd_format_version"]:
        if key in metadata:
            metadata[key.replace("nbrmd", "jupytext")] = metadata.pop(key)

    jupytext_metadata = metadata.get("jupytext", {})

    if "jupytext_formats" in metadata:
        jupytext_metadata["formats"] = metadata.pop("jupytext_formats")
    if "jupytext_format_version" in metadata:
        jupytext_metadata["text_representation"] = {"format_version": metadata.pop("jupytext_format_version")}
    if "main_language" in metadata:
        jupytext_metadata["main_language"] = metadata.pop("main_language")
    for entry in ["encoding", "executable"]:
        if entry in metadata:
            jupytext_metadata[entry] = metadata.pop(entry)

    filters = jupytext_metadata.pop("metadata_filter", {})
    if "notebook" in filters:
        jupytext_metadata["notebook_metadata_filter"] = filters["notebook"]
    if "cells" in filters:
        jupytext_metadata["cell_metadata_filter"] = filters["cells"]

    for filter_level in ["notebook_metadata_filter", "cell_metadata_filter"]:
        if filter_level in jupytext_metadata:
            jupytext_metadata[filter_level] = metadata_filter_as_string(jupytext_metadata[filter_level])

    if jupytext_metadata.get("text_representation", {}).get("jupytext_version", "").startswith("0."):
        formats = jupytext_metadata.get("formats")
        if formats:
            jupytext_metadata["formats"] = ",".join(["." + fmt if fmt.rfind(".") > 0 else fmt for fmt in formats.split(",")])

    # auto to actual extension
    formats = jupytext_metadata.get("formats")
    if formats:
        jupytext_metadata["formats"] = short_form_multiple_formats(long_form_multiple_formats(formats, metadata))

    if jupytext_metadata:
        metadata["jupytext"] = jupytext_metadata

