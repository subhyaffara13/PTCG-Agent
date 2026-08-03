import os

def notebook_to_qmd(notebook):
    """Convert a Jupyter notebook to its Quarto Markdown representation"""
    raise_if_quarto_is_not_available()
    tmp_ipynb_file = tempfile.NamedTemporaryFile(delete=False, suffix=".ipynb")
    tmp_ipynb_file.write(ipynb_writes(notebook).encode("utf-8"))
    tmp_ipynb_file.close()

    quarto("convert --log-level warning", tmp_ipynb_file.name)

    tmp_qmd_file_name = tmp_ipynb_file.name[:-6] + ".qmd"

    with open(tmp_qmd_file_name, encoding="utf-8") as qmd_file:
        text = qmd_file.read()

    os.unlink(tmp_ipynb_file.name)
    os.unlink(tmp_qmd_file_name)

    return "\n".join(text.splitlines())

