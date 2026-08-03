import os

def md_to_notebook(text):
    """Convert a Markdown text to a Jupyter notebook, using Pandoc"""
    raise_if_pandoc_is_not_available()
    tmp_file = tempfile.NamedTemporaryFile(delete=False)
    tmp_file.write(text.encode("utf-8"))
    tmp_file.close()

    if parse(pandoc_version()) < parse("2.11.2"):
        pandoc_args = "--from markdown --to ipynb -s --atx-headers --wrap=preserve --preserve-tabs"
    else:
        pandoc_args = "--from markdown --to ipynb -s --markdown-headings=atx --wrap=preserve --preserve-tabs"
    pandoc(
        pandoc_args,
        tmp_file.name,
        tmp_file.name,
    )

    with open(tmp_file.name, encoding="utf-8") as opened_file:
        notebook = ipynb_reads(opened_file.read(), as_version=4)
    os.unlink(tmp_file.name)

    return notebook

