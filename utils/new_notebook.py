
def new_notebook(cells=None):
    """Create a notebook by name, id and a list of worksheets."""
    nb = NotebookNode()
    if cells is not None:
        nb.cells = cells
    else:
        nb.cells = []
    return nb


def new_notebook(metadata=None, worksheets=None):
    """Create a notebook by name, id and a list of worksheets."""
    nb = NotebookNode()
    nb.nbformat = 2
    if worksheets is None:
        nb.worksheets = []
    else:
        nb.worksheets = list(worksheets)
    if metadata is None:
        nb.metadata = new_metadata()
    else:
        nb.metadata = NotebookNode(metadata)
    return nb


def new_notebook(name=None, metadata=None, worksheets=None):
    """Create a notebook by name, id and a list of worksheets."""
    nb = NotebookNode()
    nb.nbformat = nbformat
    nb.nbformat_minor = nbformat_minor
    if worksheets is None:
        nb.worksheets = []
    else:
        nb.worksheets = list(worksheets)
    if metadata is None:
        nb.metadata = new_metadata()
    else:
        nb.metadata = NotebookNode(metadata)
    if name is not None:
        nb.metadata.name = str_passthrough(name)
    return nb


def new_notebook(**kwargs):
    """Create a new notebook"""
    nb = NotebookNode(
        nbformat=nbformat,
        nbformat_minor=nbformat_minor,
        metadata=NotebookNode(),
        cells=[],
    )
    nb.update(kwargs)
    validate(nb)
    return nb

