
def parse_filename(fname):
    """Parse a notebook filename.

    This function takes a notebook filename and returns the notebook
    format (json/py) and the notebook name. This logic can be
    summarized as follows:

    * notebook.ipynb -> (notebook.ipynb, notebook, json)
    * notebook.json  -> (notebook.json, notebook, json)
    * notebook.py    -> (notebook.py, notebook, py)
    * notebook       -> (notebook.ipynb, notebook, json)

    Parameters
    ----------
    fname : unicode
        The notebook filename. The filename can use a specific filename
        extension (.ipynb, .json, .py) or none, in which case .ipynb will
        be assumed.

    Returns
    -------
    (fname, name, format) : (unicode, unicode, unicode)
        The filename, notebook name and format.
    """
    basename, ext = os.path.splitext(fname)  # noqa: PTH122
    if ext in [".ipynb", ".json"]:
        format_ = "json"
    elif ext == ".py":
        format_ = "py"
    else:
        basename = fname
        fname = fname + ".ipynb"
        format_ = "json"
    return fname, basename, format_


def parse_filename(fname):
    """Parse a notebook filename.

    This function takes a notebook filename and returns the notebook
    format (json/py) and the notebook name. This logic can be
    summarized as follows:

    * notebook.ipynb -> (notebook.ipynb, notebook, json)
    * notebook.json  -> (notebook.json, notebook, json)
    * notebook.py    -> (notebook.py, notebook, py)
    * notebook       -> (notebook.ipynb, notebook, json)

    Parameters
    ----------
    fname : unicode
        The notebook filename. The filename can use a specific filename
        extension (.ipynb, .json, .py) or none, in which case .ipynb will
        be assumed.

    Returns
    -------
    (fname, name, format) : (unicode, unicode, unicode)
        The filename, notebook name and format.
    """
    basename, ext = os.path.splitext(fname)  # noqa: PTH122
    if ext in [".ipynb", ".json"]:
        format_ = "json"
    elif ext == ".py":
        format_ = "py"
    else:
        basename = fname
        fname = fname + ".ipynb"
        format_ = "json"
    return fname, basename, format_

