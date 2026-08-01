
def new_raw_cell(source="", **kwargs):
    """Create a new raw cell"""
    cell = NotebookNode(
        id=random_cell_id(),
        cell_type="raw",
        source=source,
        metadata=NotebookNode(),
    )
    cell.update(kwargs)

    validate(cell, "raw_cell")
    return cell

