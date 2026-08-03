import copy

def combine_inputs_with_outputs(nb_source, nb_outputs, fmt=None):
    """Return a notebook that combines the text and metadata from the first notebook,
    with the outputs and metadata of the second notebook."""
    # nbformat version number taken from the notebook with outputs
    assert nb_outputs.nbformat == nb_source.nbformat, (
        "The notebook with outputs is in format {}.{}, please upgrade it to {}.x".format(
            nb_outputs.nbformat, nb_outputs.nbformat_minor, nb_source.nbformat
        )
    )
    nb_source.nbformat_minor = nb_outputs.nbformat_minor

    fmt = long_form_one_format(fmt)
    text_repr = nb_source.metadata.get("jupytext", {}).get("text_representation", {})
    ext = fmt.get("extension") or text_repr.get("extension")
    format_name = fmt.get("format_name") or text_repr.get("format_name")

    notebook_metadata_filter = nb_source.metadata.get("jupytext", {}).get("notebook_metadata_filter")
    if notebook_metadata_filter == "-all":
        nb_metadata = nb_outputs.metadata

    else:
        nb_metadata = restore_filtered_metadata(
            nb_source.metadata,
            nb_outputs.metadata,
            notebook_metadata_filter,
            _DEFAULT_NOTEBOOK_METADATA,
        )

    source_is_md_version_one = ext in [".md", ".markdown", ".Rmd"] and text_repr.get("format_version") == "1.0"
    if nb_metadata.get("jupytext", {}).get("formats") or ext in [
        ".md",
        ".markdown",
        ".Rmd",
    ]:
        nb_metadata.get("jupytext", {}).pop("text_representation", None)

    if not nb_metadata.get("jupytext", {}):
        nb_metadata.pop("jupytext", {})

    if format_name in ["nomarker", "sphinx", "marimo"] or source_is_md_version_one:
        cell_metadata_filter = "-all"
    else:
        cell_metadata_filter = nb_metadata.get("jupytext", {}).get("cell_metadata_filter")

    outputs_map = map_outputs_to_inputs(nb_source.cells, nb_outputs.cells)

    cells = []
    for source_cell, j in zip(nb_source.cells, outputs_map):
        if j is None:
            cells.append(source_cell)
            continue

        output_cell = nb_outputs.cells[j]

        # Outputs and optional attributes are taken from the notebook with outputs
        cell = copy(output_cell)

        # Cell text is taken from the source notebook
        cell.source = source_cell.source

        # We also restore the cell metadata that has been filtered
        cell.metadata = restore_filtered_metadata(
            source_cell.metadata,
            output_cell.metadata,
            # The 'spin' format does not allow metadata on non-code cells
            ("-all" if format_name == "spin" and source_cell.cell_type != "code" else cell_metadata_filter),
            _IGNORE_CELL_METADATA,
        )

        cells.append(cell)

    # We call NotebookNode rather than new_notebook as we don't want to validate
    # the notebook (some of the notebook in the collection of test notebooks
    # do have some invalid properties - probably inherited from an older version
    # of the notebook format).
    return NotebookNode(
        cells=cells,
        metadata=nb_metadata,
        nbformat=nb_outputs.nbformat,
        nbformat_minor=nb_outputs.nbformat_minor,
    )

