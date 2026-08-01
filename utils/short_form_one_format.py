
def short_form_one_format(jupytext_format: dict[str, str]) -> str:
    """Represent one jupytext format as a string"""
    if not isinstance(jupytext_format, dict):
        return jupytext_format
    fmt = jupytext_format["extension"]
    if "suffix" in jupytext_format:
        fmt = jupytext_format["suffix"] + fmt
    elif fmt.startswith("."):
        fmt = fmt[1:]

    if "prefix" in jupytext_format:
        fmt = jupytext_format["prefix"] + "/" + fmt

    if jupytext_format.get("format_name"):
        if jupytext_format["extension"] not in [
            ".md",
            ".markdown",
            ".Rmd",
        ] or jupytext_format["format_name"] in ["pandoc", MYST_FORMAT_NAME]:
            fmt = fmt + ":" + jupytext_format["format_name"]

    return fmt

