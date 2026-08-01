
def new_worksheet(name=None, cells=None):
    """Create a worksheet by name with with a list of cells."""
    ws = NotebookNode()
    if name is not None:
        ws.name = str(name)
    if cells is None:
        ws.cells = []
    else:
        ws.cells = list(cells)
    return ws


def new_worksheet(name=None, cells=None, metadata=None):
    """Create a worksheet by name with with a list of cells."""
    ws = NotebookNode()
    if cells is None:
        ws.cells = []
    else:
        ws.cells = list(cells)
    ws.metadata = NotebookNode(metadata or {})
    return ws

