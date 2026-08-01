
def new_markdown_cell(source="", **kwargs):
    """Create a new markdown cell"""
    cell = NotebookNode(
        id=random_cell_id(),
        cell_type="markdown",
        source=source,
        metadata=NotebookNode(),
    )
    cell.update(kwargs)

    validate(cell, "markdown_cell")
    return cell

