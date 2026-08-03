import os

def assert_conversion_same_as_mirror(nb_file, fmt, mirror_name, compare_notebook=False):
    """This function is used in the tests"""
    dirname, basename = os.path.split(nb_file)
    file_name, org_ext = os.path.splitext(basename)
    fmt = long_form_one_format(fmt)
    notebook = read(nb_file, fmt=fmt)
    fmt = check_auto_ext(fmt, notebook.metadata, "")
    ext = fmt["extension"]
    mirror_file = os.path.join(dirname, "..", "..", "outputs", mirror_name, full_path(file_name, fmt))

    # it's better not to have Jupytext metadata in test notebooks:
    if fmt == "ipynb" and "jupytext" in notebook.metadata:  # pragma: no cover
        notebook.metadata.pop("jupytext")
        write(nb_file, fmt=fmt)

    create_mirror_file_if_missing(mirror_file, notebook, fmt)

    # Compare the text representation of the two notebooks
    if compare_notebook:
        # Read and convert the mirror file to the latest nbformat version if necessary
        nb_mirror = read(mirror_file, as_version=notebook.nbformat)
        nb_mirror.nbformat_minor = notebook.nbformat_minor
        compare_notebooks(nb_mirror, notebook)
        return
    elif ext == ".ipynb":
        notebook = read(mirror_file)
        fmt.update({"extension": org_ext})
        actual = writes(notebook, fmt)
        with open(nb_file, encoding="utf-8") as fp:
            expected = fp.read()
    else:
        actual = writes(notebook, fmt)
        with open(mirror_file, encoding="utf-8") as fp:
            expected = fp.read()

    if not actual.endswith("\n"):
        actual = actual + "\n"

    if fmt.get("format_name") == "marimo":
        lines = expected.splitlines()
        lines = [
            # mirror files were generated with marimo 0.17.8
            f'__generated_with = "{marimo_version()}"' if line == '__generated_with = "0.17.8"' else line
            for line in lines
        ]
        expected = "\n".join(lines) + "\n"

    compare(actual, expected)

    # Compare the two notebooks
    if ext != ".ipynb":
        notebook = read(nb_file)
        nb_mirror = read(mirror_file, fmt=fmt)

        if fmt.get("format_name") == "sphinx":
            nb_mirror.cells = nb_mirror.cells[1:]
            for cell in notebook.cells:
                cell.metadata = {}
            for cell in nb_mirror.cells:
                cell.metadata = {}

        compare_notebooks(nb_mirror, notebook, fmt)

        nb_mirror = combine_inputs_with_outputs(nb_mirror, notebook)
        compare_notebooks(nb_mirror, notebook, fmt, compare_outputs=True)

