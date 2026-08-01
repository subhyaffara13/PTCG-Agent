
def new_text_cell(text=None):
    """Create a new text cell."""
    cell = NotebookNode()
    if text is not None:
        cell.text = str(text)
    cell.cell_type = "text"
    return cell


def new_text_cell(cell_type, source=None, rendered=None):
    """Create a new text cell."""
    cell = NotebookNode()
    if source is not None:
        cell.source = str(source)
    if rendered is not None:
        cell.rendered = str(rendered)
    cell.cell_type = cell_type
    return cell


def new_text_cell(cell_type, source=None, rendered=None, metadata=None):
    """Create a new text cell."""
    cell = NotebookNode()
    # VERSIONHACK: plaintext -> raw
    # handle never-released plaintext name for raw cells
    if cell_type == "plaintext":
        cell_type = "raw"
    if source is not None:
        cell.source = str_passthrough(source)
    cell.metadata = NotebookNode(metadata or {})
    cell.cell_type = cell_type
    return cell

