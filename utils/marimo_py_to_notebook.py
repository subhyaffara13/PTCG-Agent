import os

def marimo_py_to_notebook(text):
    """Convert a Marimo script to a Jupyter notebook, using Marimo"""
    raise_if_marimo_is_not_available()

    # On Windows, NamedTemporaryFile cannot be reopened with open,
    # so we keep the file names and close the files
    tmp_py_file = tempfile.NamedTemporaryFile(suffix=".py")
    tmp_py_file_name = tmp_py_file.name
    tmp_py_file.close()

    tmp_ipynb_file = tempfile.NamedTemporaryFile(suffix=".ipynb")
    tmp_ipynb_file_name = tmp_ipynb_file.name
    tmp_ipynb_file.close()

    with open(tmp_py_file_name, "w") as fp:
        fp.write(text)

    marimo(
        "export",
        "ipynb",
        # Keep the current order to minimize diffs on round trips
        "--sort",
        "top-down",
        tmp_py_file_name,
        "-o",
        tmp_ipynb_file_name,
    )

    notebook = nbformat.read(tmp_ipynb_file_name, as_version=4)

    os.remove(tmp_py_file_name)
    os.remove(tmp_ipynb_file_name)

    # In the following we revert some of the side effects of the marimo conversion
    # to ensure stability of the round trip. Not all the side effects are reverted.

    # You can test the round trip for a given document with:
    #   jupytext --test --to py:marimo your_notebook.ipynb
    # or with:
    #   jupytext --test --to ipynb your_marimo_script.py

    # Ideally these round trip issues should be fixed in Marimo itself - please report them at
    # https://github.com/marimo/marimo/issues and optionally mention @mwouts (author of Jupytext)
    # in the issue description.
    import_marimo_cell = "import marimo as mo"
    need_to_remove_import_marimo_cell = False

    for cell in notebook.cells:
        if cell.cell_type != "code":
            continue
        matplotlib_inline_comment = "# '%matplotlib inline' command supported automatically in marimo"
        if cell.source.startswith(matplotlib_inline_comment):
            cell.source = "%matplotlib inline" + cell.source.removeprefix(matplotlib_inline_comment)
        if cell.source == import_marimo_cell:
            need_to_remove_import_marimo_cell = True
        if cell.source.startswith("# Cell tags:"):
            if "\n" not in cell.source:
                cell.source += "\n"
            tag_line, cell.source = cell.source.split("\n", 1)
            tags = tag_line.removeprefix("# Cell tags:").strip().split(", ")
            cell.metadata["tags"] = tags

    if need_to_remove_import_marimo_cell:
        notebook.cells = [cell for cell in notebook.cells if cell.source != import_marimo_cell]

    return notebook

