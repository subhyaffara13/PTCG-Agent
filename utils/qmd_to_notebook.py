
def qmd_to_notebook(text):
    """Convert a Quarto Markdown notebook to a Jupyter notebook"""
    raise_if_quarto_is_not_available()
    tmp_qmd_file = tempfile.NamedTemporaryFile(delete=False, suffix=".qmd")
    tmp_qmd_file.write(text.encode("utf-8"))
    tmp_qmd_file.close()

    quarto("convert --log-level warning", tmp_qmd_file.name)

    tmp_ipynb_file_name = tmp_qmd_file.name[:-4] + ".ipynb"

    with open(tmp_ipynb_file_name, encoding="utf-8") as ipynb_file:
        notebook = ipynb_reads(ipynb_file.read(), as_version=4)

    os.unlink(tmp_qmd_file.name)
    os.unlink(tmp_ipynb_file_name)

    # Recent version of Quarto duplicate the notebook metadata in a YAML header
    # If we find such a header, we remove it if it is identical to the notebook metadata
    if not notebook.cells or notebook.cells[0].cell_type != "markdown":
        return notebook

    cell_source = notebook.cells[0].source.strip()
    if cell_source.startswith("---") and cell_source.endswith("---"):
        try:
            metadata_from_top_cell = yaml.safe_load(cell_source[3:-3])
        except yaml.YAMLError:
            pass
        else:
            if "jupyter" not in metadata_from_top_cell:
                return notebook
            if metadata_from_top_cell == {"jupyter": "python3"}:
                # Quarto sometimes writes "jupyter: python3" instead of the full metadata
                # We can safely remove this cell
                del notebook.cells[0]
                return notebook

            jupyter_metadata = json.dumps(metadata_from_top_cell["jupyter"], sort_keys=True)
            notebook_metadata = json.dumps(notebook.metadata, sort_keys=True)
            if jupyter_metadata == notebook_metadata:
                if set(metadata_from_top_cell.keys()) == {"jupyter"}:
                    # The metadata are identical, we can remove the duplicated cell
                    del notebook.cells[0]
                    return notebook
                else:
                    # The jupyter metadata are identical, but there are other keys in the YAML header
                    # We keep the cell, but remove the jupyter key
                    lines = cell_source.splitlines()
                    non_jupyter_lines = []
                    in_jupyter_section = False
                    for line in lines:
                        if not (line.startswith("  ") or line.startswith("\t")):
                            in_jupyter_section = False
                        if line.rstrip() == "jupyter:":
                            in_jupyter_section = True
                        if not in_jupyter_section:
                            non_jupyter_lines.append(line)
                    notebook.cells[0].source = "\n".join(non_jupyter_lines)
            else:
                # The metadata are different, we keep the cell but issue a warning
                print(
                    "Warning: the Quarto Markdown file contains a YAML header that does not match the notebook metadata:\n"
                    f"Header metadata:\n{metadata_from_top_cell}\n"
                    f"Notebook metadata:\n{notebook_metadata}",
                    file=sys.stderr,
                )

    return notebook

