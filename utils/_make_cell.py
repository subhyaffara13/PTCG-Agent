
def _make_cell(value=_empty_cell_value):
    cell = _make_empty_cell()
    if value is not _empty_cell_value:
        cell.cell_contents = value
    return cell

