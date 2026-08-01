
def short_form_multiple_formats(jupytext_formats: list[dict[str, str]]) -> str:
    """Convert jupytext formats, represented as a list of dictionaries, to a comma separated list"""
    if not isinstance(jupytext_formats, list):
        return jupytext_formats

    jupytext_formats = [short_form_one_format(fmt) for fmt in jupytext_formats]
    return ",".join(jupytext_formats)

