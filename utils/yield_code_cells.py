
def yield_code_cells(nb):
    """Iterator that yields all cells in a notebook

    nbformat version independent
    """
    if nb.nbformat >= 4:
        for cell in nb["cells"]:
            if cell["cell_type"] == "code":
                yield cell
    elif nb.nbformat == 3:
        for ws in nb["worksheets"]:
            for cell in ws["cells"]:
                if cell["cell_type"] == "code":
                    yield cell

