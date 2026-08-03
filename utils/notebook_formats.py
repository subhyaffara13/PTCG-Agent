import os

def notebook_formats(nbk, config, path, fallback_on_current_fmt=True):
    """Return the list of formats for the current notebook"""
    metadata = nbk.get("metadata")
    jupytext_metadata = metadata.get("jupytext", {})
    formats = jupytext_metadata.get("formats") or metadata.get("jupytext_formats")

    if formats:
        formats = long_form_multiple_formats(formats, metadata, auto_ext_requires_language_info=False)
    elif config:
        current_format = jupytext_metadata.get("text_representation", {"extension": os.path.splitext(path)[1]})
        default_formats = long_form_multiple_formats(
            config.default_formats(path),
            metadata,
            auto_ext_requires_language_info=False,
        )

        if any(
            current_format.get("extension") == fmt["extension"]
            and (
                "format_name" not in fmt
                or "format_name" not in current_format
                or current_format["format_name"] == fmt.get("format_name")
            )
            for fmt in default_formats
        ):
            formats = default_formats

    if not formats:
        if not fallback_on_current_fmt:
            return None
        text_repr = jupytext_metadata.get("text_representation", {})
        ext = os.path.splitext(path)[1]
        fmt = {"extension": ext}

        if ext == text_repr.get("extension") and text_repr.get("format_name"):
            fmt["format_name"] = text_repr.get("format_name")

        formats = [fmt]

    # Set preferred formats if no format name has been given yet
    if config:
        formats = [preferred_format(f, config.preferred_jupytext_formats_save) for f in formats]

    return formats

