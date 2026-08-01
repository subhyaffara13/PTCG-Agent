
def notebook_to_marimo_py(notebook):
    """Convert a notebook to its Marimo script"""
    raise_if_marimo_is_not_available()

    # On Windows, NamedTemporaryFile cannot be reopened with open,
    # so we keep the file names and close the files
    tmp_py_file = tempfile.NamedTemporaryFile(suffix=".py", delete=False)
    tmp_py_file_name = tmp_py_file.name
    tmp_py_file.close()

    tmp_ipynb_file = tempfile.NamedTemporaryFile(suffix=".ipynb", delete=False)
    tmp_ipynb_file_name = tmp_ipynb_file.name
    tmp_ipynb_file.close()

    with open(tmp_ipynb_file_name, "w") as fp:
        nbformat.write(notebook, fp)

    marimo("convert", tmp_ipynb_file_name, "-o", tmp_py_file_name)

    with open(tmp_py_file_name) as fp:
        text = fp.read()

    os.remove(tmp_ipynb_file_name)
    os.remove(tmp_py_file_name)

    return "\n".join(text.splitlines())

