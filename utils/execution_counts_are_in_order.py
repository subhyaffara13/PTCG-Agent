
def execution_counts_are_in_order(notebook):
    """Returns True if all the code cells have an execution count, ordered from 1 to N with no missing number"""
    expected_execution_count = 1
    for cell in notebook.cells:
        if cell.cell_type == "code":
            if cell.execution_count != expected_execution_count:
                return False
            expected_execution_count += 1
    return True

