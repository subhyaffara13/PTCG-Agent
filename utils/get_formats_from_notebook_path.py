
def get_formats_from_notebook_path(nb_file, fmt=None):
    """
    Return the paired formats for a given notebook in the extended form.

    Parameters
    ----------
    nb_file : str
        Path to the notebook file.
    fmt : dict or None, optional
        The Jupytext format specification (default is None).

    Returns
    -------
    list of dict
        The paired formats in the 'extended form', i.e., as a list of dictionaries
        where each dictionary fully specifies a format (including extension, format_name, etc.).
    """
    config = load_jupytext_config(nb_file)
    notebook = read(nb_file, fmt=fmt, config=config)
    return get_formats_from_notebook_and_config(notebook, config, nb_file)

