
def _get_cell_contents(cell):
    try:
        return cell.cell_contents
    except ValueError:
        # Handle empty cells explicitly with a sentinel value.
        return _empty_cell_value

