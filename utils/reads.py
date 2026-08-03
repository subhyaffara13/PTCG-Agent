import copy

def reads(text, fmt=None, as_version=nbformat.NO_CONVERT, config=None, **kwargs):
    """
    Read a notebook from a string

    :param text: the text representation of the notebook
    :param fmt: (optional) the jupytext format like `md`, `py:percent`, ...
    :param as_version: see nbformat.reads
    :param config: (optional) a Jupytext configuration object
    :param kwargs: (not used) additional parameters for nbformat.reads
    :return: the notebook
    """
    fmt = copy(fmt) if fmt else divine_format(text)
    fmt = long_form_one_format(fmt)
    ext = fmt["extension"]

    if ext == ".ipynb":
        nb = nbformat.reads(text, as_version, **kwargs)
        (version, version_minor) = nbformat.reader.get_version(nb)
        if version != 4:
            warnings.warn(
                f"Notebooks in nbformat version {version}.{version_minor} are not supported by Jupytext. "
                f"Please consider converting them to nbformat version 4.x with "
                f"'jupyter nbconvert --to notebook --inplace'"
            )
        return nb

    format_name = read_format_from_metadata(text, ext) or fmt.get("format_name")

    if format_name:
        format_options = {}
    else:
        format_name, format_options = guess_format(text, ext)

    if format_name:
        fmt["format_name"] = format_name

    fmt.update(format_options)
    reader = TextNotebookConverter(fmt, config)
    notebook = reader.reads(text, **kwargs)
    rearrange_jupytext_metadata(notebook.metadata)

    if format_name and insert_or_test_version_number():
        notebook.metadata.setdefault("jupytext", {}).setdefault("text_representation", {}).update(
            {"extension": ext, "format_name": format_name}
        )

    return notebook


def reads(s, format="DEPRECATED", version=current_nbformat, **kwargs):
    """Read a notebook from a string and return the NotebookNode object.

    This function properly handles notebooks of any version. The notebook
    returned will always be in the current version's format.

    Parameters
    ----------
    s : unicode
        The raw unicode string to read the notebook from.

    Returns
    -------
    nb : NotebookNode
        The notebook that was read.
    """
    if format not in {"DEPRECATED", "json"}:
        _warn_format()
    nb = reader_reads(s, **kwargs)
    nb = convert(nb, version)
    try:
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=DeprecationWarning)
            validate(nb, repair_duplicate_cell_ids=False)
    except ValidationError as e:
        get_logger().error("Notebook JSON is invalid: %s", e)
    return nb


def reads(s, **kwargs):
    """Read a notebook from a json string and return the
    NotebookNode object.

    This function properly reads notebooks of any version.  No version
    conversion is performed.

    Parameters
    ----------
    s : unicode | bytes
        The raw string or bytes object to read the notebook from.

    Returns
    -------
    nb : NotebookNode
        The notebook that was read.

    Raises
    ------
    ValidationError
        Notebook JSON for a given version is missing an expected key and cannot be read.
    NBFormatError
        Specified major version is invalid or unsupported.
    """
    from . import NBFormatError, versions

    nb_dict = parse_json(s, **kwargs)
    (major, minor) = get_version(nb_dict)
    if major in versions:
        try:
            return versions[major].to_notebook_json(nb_dict, minor=minor)
        except AttributeError as e:
            msg = f"The notebook is invalid and is missing an expected key: {e}"
            raise ValidationError(msg) from None
    else:
        raise NBFormatError("Unsupported nbformat version %s" % major)


def reads(s, as_version, capture_validation_error=None, **kwargs):
    """Read a notebook from a string and return the NotebookNode object as the given version.

    The string can contain a notebook of any version.
    The notebook will be returned `as_version`, converting, if necessary.

    Notebook format errors will be logged.

    Parameters
    ----------
    s : unicode
        The raw unicode string to read the notebook from.
    as_version : int
        The version of the notebook format to return.
        The notebook will be converted, if necessary.
        Pass nbformat.NO_CONVERT to prevent conversion.
    capture_validation_error : dict, optional
        If provided, a key of "ValidationError" with a
        value of the ValidationError instance will be added
        to the dictionary.

    Returns
    -------
    nb : NotebookNode
        The notebook that was read.
    """
    nb = reader.reads(s, **kwargs)
    if as_version is not NO_CONVERT:
        nb = convert(nb, as_version)
    try:
        validate(nb)
    except ValidationError as e:
        get_logger().error("Notebook JSON is invalid: %s", e)
        if isinstance(capture_validation_error, dict):
            capture_validation_error["ValidationError"] = e
    return nb


def reads(s, **kwargs):
    """REMOVED"""
    raise Exception(REMOVED_MSG)

