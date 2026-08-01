
def compare_notebooks(
    notebook_actual,
    notebook_expected,
    fmt=None,
    allow_expected_differences=True,
    raise_on_first_difference=True,
    compare_outputs=False,
    compare_ids=None,
):
    """Compare the two notebooks, and raise with a meaningful message
    that explains the differences, if any"""
    fmt = long_form_one_format(fmt)
    format_name = fmt.get("format_name")

    if format_name == "sphinx" and notebook_actual.cells and notebook_actual.cells[0].source == "%matplotlib inline":
        notebook_actual.cells = notebook_actual.cells[1:]

    if compare_ids is None:
        compare_ids = compare_outputs

    modified_cells, modified_cell_metadata = compare_cells(
        notebook_actual.cells,
        notebook_expected.cells,
        raise_on_first_difference,
        compare_outputs=compare_outputs,
        compare_ids=compare_ids,
        cell_metadata_filter="-all"
        if format_name == "marimo"
        else notebook_actual.get("jupytext", {}).get("cell_metadata_filter"),
        allow_missing_code_cell_metadata=(allow_expected_differences and format_name in ["sphinx", "marimo"]),
        allow_missing_markdown_cell_metadata=(allow_expected_differences and format_name in ["sphinx", "spin", "marimo"]),
        allow_filtered_cell_metadata=allow_expected_differences,
        allow_removed_final_blank_line=allow_expected_differences,
    )

    # Compare notebook metadata
    modified_metadata = False
    if fmt.get("format_name") != "marimo":
        try:
            ignore_kernelspec = fmt.get("extension") == ".qmd" and allow_expected_differences
            compare(
                filtered_notebook_metadata(notebook_actual, ignore_kernelspec),
                filtered_notebook_metadata(notebook_expected, ignore_kernelspec),
            )
        except AssertionError as error:
            if raise_on_first_difference:
                raise NotebookDifference(f"Notebook metadata differ: {str(error)}")
            modified_metadata = True

    error = []
    if modified_cells:
        error.append(
            "Cells {} differ ({}/{})".format(
                ",".join([str(i) for i in modified_cells]),
                len(modified_cells),
                len(notebook_expected.cells),
            )
        )
    if modified_cell_metadata:
        error.append("Cell metadata '{}' differ".format("', '".join([str(i) for i in modified_cell_metadata])))
    if modified_metadata:
        error.append("Notebook metadata differ")

    if error:
        raise NotebookDifference(" | ".join(error))

