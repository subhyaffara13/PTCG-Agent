
def notebook_to_md(notebook):
    """Convert a notebook to its Markdown representation, using Pandoc"""
    raise_if_pandoc_is_not_available()
    tmp_file = tempfile.NamedTemporaryFile(delete=False)
    tmp_file.write(ipynb_writes(notebook).encode("utf-8"))
    tmp_file.close()

    if parse(pandoc_version()) < parse("2.11.2"):
        pandoc_args = "--from ipynb --to markdown -s --atx-headers --wrap=preserve --preserve-tabs"
    else:
        pandoc_args = "--from ipynb --to markdown -s --markdown-headings=atx --wrap=preserve --preserve-tabs"
    pandoc(
        pandoc_args,
        tmp_file.name,
        tmp_file.name,
    )

    with open(tmp_file.name, encoding="utf-8") as opened_file:
        text = opened_file.read()

    os.unlink(tmp_file.name)
    return "\n".join(text.splitlines())

