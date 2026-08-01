
def upgrade(nb, orig_version=None):
    """Upgrade a notebook."""
    msg = "Cannot convert to v1 notebook format"
    raise ValueError(msg)


def upgrade(nb, from_version=1):
    """Convert a notebook to the v2 format.

    Parameters
    ----------
    nb : NotebookNode
        The Python representation of the notebook to convert.
    from_version : int
        The version of the notebook to convert from.
    """
    if from_version == 1:
        newnb = new_notebook()
        ws = new_worksheet()
        for cell in nb.cells:
            if cell.cell_type == "code":
                newcell = new_code_cell(
                    input=cell.get("code"), prompt_number=cell.get("prompt_number")
                )
            elif cell.cell_type == "text":
                newcell = new_text_cell("markdown", source=cell.get("text"))
            ws.cells.append(newcell)
        newnb.worksheets.append(ws)
        return newnb

    raise ValueError("Cannot convert a notebook from v%s to v2" % from_version)


def upgrade(nb, from_version=2, from_minor=0):
    """Convert a notebook to v3.

    Parameters
    ----------
    nb : NotebookNode
        The Python representation of the notebook to convert.
    from_version : int
        The original version of the notebook to convert.
    from_minor : int
        The original minor version of the notebook to convert (only relevant for v >= 3).
    """
    if from_version == 2:
        # Mark the original nbformat so consumers know it has been converted.
        nb.nbformat = nbformat
        nb.nbformat_minor = nbformat_minor

        nb.orig_nbformat = 2
        nb = _unbytes(nb)
        for ws in nb["worksheets"]:
            for cell in ws["cells"]:
                cell.setdefault("metadata", {})
        return nb
    if from_version == 3:
        if from_minor != nbformat_minor:
            nb.orig_nbformat_minor = from_minor
        nb.nbformat_minor = nbformat_minor
        return nb
    msg = (
        "Cannot convert a notebook directly from v%s to v3.  "
        "Try using the nbformat.convert module." % from_version
    )
    raise ValueError(msg)


def upgrade(nb, from_version=None, from_minor=None):
    """Convert a notebook to latest v4.

    Parameters
    ----------
    nb : NotebookNode
        The Python representation of the notebook to convert.
    from_version : int
        The original version of the notebook to convert.
    from_minor : int
        The original minor version of the notebook to convert (only relevant for v >= 3).
    """
    if not from_version:
        from_version = nb["nbformat"]
    if not from_minor:
        if "nbformat_minor" not in nb:
            if from_version == 4:
                msg = "The v4 notebook does not include the nbformat minor, which is needed."
                raise validator.ValidationError(msg)
            from_minor = 0
        else:
            from_minor = nb["nbformat_minor"]

    if from_version == 3:
        # Validate the notebook before conversion
        _warn_if_invalid(nb, from_version)

        # Mark the original nbformat so consumers know it has been converted
        orig_nbformat = nb.pop("orig_nbformat", None)
        orig_nbformat_minor = nb.pop("orig_nbformat_minor", None)
        nb.metadata.orig_nbformat = orig_nbformat or 3
        nb.metadata.orig_nbformat_minor = orig_nbformat_minor or 0

        # Mark the new format
        nb.nbformat = nbformat
        nb.nbformat_minor = nbformat_minor

        # remove worksheet(s)
        nb["cells"] = cells = []
        # In the unlikely event of multiple worksheets,
        # they will be flattened
        for ws in nb.pop("worksheets", []):
            # upgrade each cell
            for cell in ws["cells"]:
                cells.append(upgrade_cell(cell))
        # upgrade metadata
        nb.metadata.pop("name", "")
        nb.metadata.pop("signature", "")
        # Validate the converted notebook before returning it
        _warn_if_invalid(nb, nbformat)
        return nb
    if from_version == 4:
        if from_minor == nbformat_minor:
            return nb

        # other versions migration code e.g.
        # if from_minor < 3:
        # if from_minor < 4:

        if from_minor < 5:
            for cell in nb.cells:
                cell.id = random_cell_id()

        nb.metadata.orig_nbformat_minor = from_minor
        nb.nbformat_minor = nbformat_minor

        return nb
    raise ValueError(
        "Cannot convert a notebook directly from v%s to v4.  "
        "Try using the nbformat.convert module." % from_version
    )

