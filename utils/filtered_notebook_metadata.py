
def filtered_notebook_metadata(notebook, ignore_kernelspec=False):
    """Notebook metadata, filtered for metadata added by Jupytext itself"""
    metadata = filter_metadata(
        notebook.metadata,
        notebook.metadata.get("jupytext", {}).get("notebook_metadata_filter"),
        _DEFAULT_NOTEBOOK_METADATA,
    )

    # Quarto round-trips may change the kernelspec
    if ignore_kernelspec:
        metadata.pop("kernelspec", None)

    if "jupytext" in metadata:
        del metadata["jupytext"]
    return metadata

