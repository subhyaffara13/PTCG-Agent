
def long_form_multiple_formats(
    jupytext_formats: str, metadata=None, auto_ext_requires_language_info=True
) -> list[dict[str, str]]:
    """Convert a concise encoding of jupytext.formats to a list of formats, encoded as dictionaries"""
    if not jupytext_formats:
        return []

    if not isinstance(jupytext_formats, list):
        jupytext_formats = [fmt for fmt in jupytext_formats.split(",") if fmt]

    jupytext_formats = [
        long_form_one_format(
            fmt,
            metadata,
            auto_ext_requires_language_info=auto_ext_requires_language_info,
        )
        for fmt in jupytext_formats
    ]

    if not auto_ext_requires_language_info:
        jupytext_formats = [fmt for fmt in jupytext_formats if fmt["extension"] != ".auto"]

    return jupytext_formats

