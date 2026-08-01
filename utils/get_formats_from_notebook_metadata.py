
def get_formats_from_notebook_metadata(notebook):
    """
    Get the pairing information from the notebook metadata.

    Parameters
    ----------
    notebook : nbformat.NotebookNode
        The notebook object whose metadata will be inspected.

    Returns
    -------
    formats : None or str
        The value of the 'formats' field in the 'jupytext' metadata, which can be None or a string.
    """
    return notebook.metadata.get("jupytext", {}).get("formats")

