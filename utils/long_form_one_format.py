
def long_form_one_format(jupytext_format, metadata=None, update=None, auto_ext_requires_language_info=True):
    """Parse 'sfx.py:percent' into {'suffix':'sfx', 'extension':'py', 'format_name':'percent'}"""
    if isinstance(jupytext_format, dict):
        if update:
            jupytext_format.update(update)
        return validate_one_format(jupytext_format)

    if not jupytext_format:
        return {}

    common_name_to_ext = {
        "notebook": "ipynb",
        "rmarkdown": "Rmd",
        "quarto": "qmd",
        "marimo": "py",
        "markdown": "md",
        "script": "auto",
        "c++": "cpp",
        "myst": "md:myst",
        "pandoc": "md:pandoc",
    }
    if jupytext_format.lower() in common_name_to_ext:
        jupytext_format = common_name_to_ext[jupytext_format.lower()]

    fmt = {}

    if jupytext_format.rfind("/") > 0:
        fmt["prefix"], jupytext_format = jupytext_format.rsplit("/", 1)

    if jupytext_format.rfind(":") >= 0:
        ext, fmt["format_name"] = jupytext_format.rsplit(":", 1)
        if fmt["format_name"] == "bare":
            warnings.warn(
                "The `bare` format has been renamed to `nomarker` - (see https://github.com/mwouts/jupytext/issues/397)",
                DeprecationWarning,
            )
            fmt["format_name"] = "nomarker"
    elif not jupytext_format or "." in jupytext_format or ("." + jupytext_format) in NOTEBOOK_EXTENSIONS + [".auto"]:
        ext = jupytext_format
    elif jupytext_format in _VALID_FORMAT_NAMES:
        fmt["format_name"] = jupytext_format
        ext = ""
    else:
        raise JupytextFormatError(
            "'{}' is not a notebook extension (one of {}), nor a notebook format (one of {})".format(
                jupytext_format,
                ", ".join(NOTEBOOK_EXTENSIONS),
                ", ".join(_VALID_FORMAT_NAMES),
            )
        )

    if ext.rfind(".") > 0:
        fmt["suffix"], ext = os.path.splitext(ext)

    if not ext.startswith("."):
        ext = "." + ext

    if ext == ".auto":
        ext = auto_ext_from_metadata(metadata) if metadata is not None else ".auto"
        if not ext:
            if auto_ext_requires_language_info:
                raise JupytextFormatError(
                    "No language information in this notebook. Please replace 'auto' with an actual script extension."
                )
            ext = ".auto"

    fmt["extension"] = ext
    if update:
        fmt.update(update)
    return validate_one_format(fmt)

