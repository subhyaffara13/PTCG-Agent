
def insert_jupytext_info_and_filter_metadata(metadata, fmt, text_format, unsupported_keys):
    """Update the notebook metadata to include Jupytext information, and filter
    the notebook metadata according to the default or user filter"""
    if insert_or_test_version_number():
        metadata.setdefault("jupytext", {})["text_representation"] = {
            "extension": fmt["extension"],
            "format_name": text_format.format_name,
            "format_version": text_format.current_version_number,
            "jupytext_version": __version__,
        }

    if "jupytext" in metadata and not metadata["jupytext"]:
        del metadata["jupytext"]

    notebook_metadata_filter = fmt.get("notebook_metadata_filter")
    return filter_metadata(
        metadata,
        notebook_metadata_filter,
        _DEFAULT_NOTEBOOK_METADATA,
        unsupported_keys=unsupported_keys,
    )

