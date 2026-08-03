import copy

def writes(notebook, fmt, version=nbformat.NO_CONVERT, config=None, **kwargs):
    """Return the text representation of the notebook

    :param notebook: the notebook
    :param fmt: the jupytext format like `md`, `py:percent`, ...
    :param version: see nbformat.writes
    :param config: (optional) a Jupytext configuration object
    :param kwargs: (not used) additional parameters for nbformat.writes
    :return: the text representation of the notebook
    """
    if version is not nbformat.NO_CONVERT:
        if not isinstance(version, int):
            raise TypeError("The argument 'version' should be either nbformat.NO_CONVERT, or an integer.")
        notebook = nbformat.convert(notebook, version)
    (version, version_minor) = nbformat.reader.get_version(notebook)
    if version < 4:
        raise NotSupportedNBFormatVersion(
            f"Notebooks in nbformat version {version}.{version_minor} are not supported by Jupytext. "
            f"Please convert your notebooks to nbformat version 4 with "
            f"'jupyter nbconvert --to notebook --inplace', or call this function with 'version=4'."
        )
    if version > 4 or (version == 4 and version_minor > 5):
        warnings.warn(
            f"Notebooks in nbformat version {version}.{version_minor} "
            f"have not been tested with Jupytext version {__version__}."
        )

    metadata = deepcopy(notebook.metadata)
    rearrange_jupytext_metadata(metadata)
    fmt = copy(fmt)
    fmt = long_form_one_format(fmt, metadata)
    ext = fmt["extension"]
    format_name = fmt.get("format_name")

    if ext == ".ipynb":
        return nbformat.writes(
            drop_text_representation_metadata(notebook, metadata),
            version,
            **kwargs,
        )

    if not format_name:
        format_name = format_name_for_ext(metadata, ext, explicit_default=False)

    # Since Jupytext==1.17, the default format for
    # writing a notebook to a script is the percent format
    if not format_name and "cell_markers" not in fmt and ext in _SCRIPT_EXTENSIONS:
        format_name = "percent"

    if format_name:
        fmt["format_name"] = format_name
        update_jupytext_formats_metadata(metadata, fmt)

    writer = TextNotebookConverter(fmt, config)
    return writer.writes(notebook, metadata)


def writes(nb, format="DEPRECATED", version=current_nbformat, **kwargs):
    """Write a notebook to a string in a given format in the current nbformat version.

    This function always writes the notebook in the current nbformat version.

    Parameters
    ----------
    nb : NotebookNode
        The notebook to write.
    version : int
        The nbformat version to write.
        Used for downgrading notebooks.

    Returns
    -------
    s : unicode
        The notebook string.
    """
    if format not in {"DEPRECATED", "json"}:
        _warn_format()
    nb = convert(nb, version)
    try:
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=DeprecationWarning)
            validate(nb, repair_duplicate_cell_ids=False)
    except ValidationError as e:
        get_logger().error("Notebook JSON is invalid: %s", e)
    return versions[version].writes_json(nb, **kwargs)


def writes(nb, version=NO_CONVERT, capture_validation_error=None, **kwargs):
    """Write a notebook to a string in a given format in the given nbformat version.

    Any notebook format errors will be logged.

    Parameters
    ----------
    nb : NotebookNode
        The notebook to write.
    version : int, optional
        The nbformat version to write.
        If unspecified, or specified as nbformat.NO_CONVERT,
        the notebook's own version will be used and no conversion performed.
    capture_validation_error : dict, optional
        If provided, a key of "ValidationError" with a
        value of the ValidationError instance will be added
        to the dictionary.

    Returns
    -------
    s : unicode
        The notebook as a JSON string.
    """
    if version is not NO_CONVERT:
        nb = convert(nb, version)
    else:
        version, _ = reader.get_version(nb)
    try:
        validate(nb)
    except ValidationError as e:
        get_logger().error("Notebook JSON is invalid: %s", e)
        if isinstance(capture_validation_error, dict):
            capture_validation_error["ValidationError"] = e
    return versions[version].writes_json(nb, **kwargs)

