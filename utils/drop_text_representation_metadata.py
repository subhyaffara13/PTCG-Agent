
def drop_text_representation_metadata(notebook, metadata=None):
    """When the notebook is saved to an ipynb file, we drop the text_representation metadata"""
    if metadata is None:
        # Make a copy to avoid modification by reference
        metadata = deepcopy(notebook["metadata"])

    jupytext_metadata = metadata.get("jupytext", {})
    jupytext_metadata.pop("text_representation", {})

    # Remove the jupytext section if empty
    if not jupytext_metadata:
        metadata.pop("jupytext", {})

    return NotebookNode(
        nbformat=notebook["nbformat"],
        nbformat_minor=notebook["nbformat_minor"],
        metadata=metadata,
        cells=notebook["cells"],
    )

