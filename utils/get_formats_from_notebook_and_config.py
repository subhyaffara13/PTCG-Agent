
def get_formats_from_notebook_and_config(notebook, config, nb_file):
    """
    Get the notebook formats from notebook metadata or config.

    Notebook metadata takes precedence over config. If the notebook metadata contains pairing information,
    it is used; otherwise, the configuration is used as a fallback.

    Parameters
    ----------
    notebook : dict
        The notebook object (as a dictionary).
    config : JupytextConfiguration or None
        The Jupytext configuration object.
    nb_file : str
        The path to the notebook file.

    Returns
    -------
    list
        A list of format dictionaries describing the notebook's paired formats.
    """
    formats = get_formats_from_notebook_metadata(notebook)
    if formats:
        return long_form_multiple_formats(formats)
    else:
        return notebook_formats(notebook, config, nb_file)

