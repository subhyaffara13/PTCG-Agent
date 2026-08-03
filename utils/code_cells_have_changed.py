import os

def code_cells_have_changed(notebook, nb_files):
    """The source for the code cells has not changed"""
    for nb_file in nb_files:
        if not os.path.exists(nb_file):
            return True

        nb_ref = read(nb_file)

        # Are the new code cells equals to those in the file?
        ref = [cell.source for cell in nb_ref.cells if cell.cell_type == "code"]
        new = [cell.source for cell in notebook.cells if cell.cell_type == "code"]

        if ref != new:
            return True

    return False

