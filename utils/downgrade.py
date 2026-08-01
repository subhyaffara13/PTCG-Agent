
def downgrade(nb):
    """Convert a v2 notebook to v1.

    Parameters
    ----------
    nb : NotebookNode
        The Python representation of the notebook to convert.
    """
    msg = "Downgrade from notebook v2 to v1 is not supported."
    raise Exception(msg)


def downgrade(nb):
    """Convert a v3 notebook to v2.

    Parameters
    ----------
    nb : NotebookNode
        The Python representation of the notebook to convert.
    """
    if nb.nbformat != 3:
        return nb
    nb.nbformat = 2
    for ws in nb.worksheets:
        for cell in ws.cells:
            if cell.cell_type == "heading":
                heading_to_md(cell)
            elif cell.cell_type == "raw":
                raw_to_md(cell)
    return nb


def downgrade(nb):
    """Convert a v4 notebook to v3.

    Parameters
    ----------
    nb : NotebookNode
        The Python representation of the notebook to convert.
    """
    if nb.nbformat != nbformat:
        return nb

    # Validate the notebook before conversion
    _warn_if_invalid(nb, nbformat)

    nb.nbformat = v3.nbformat
    nb.nbformat_minor = v3.nbformat_minor
    cells = [downgrade_cell(cell) for cell in nb.pop("cells")]
    nb.worksheets = [v3.new_worksheet(cells=cells)]
    nb.metadata.setdefault("name", "")

    # Validate the converted notebook before returning it
    _warn_if_invalid(nb, v3.nbformat)

    nb.orig_nbformat = nb.metadata.pop("orig_nbformat", nbformat)
    nb.orig_nbformat_minor = nb.metadata.pop("orig_nbformat_minor", nbformat_minor)

    return nb

