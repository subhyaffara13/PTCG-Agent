
def _get_cell_hash_content(content: types.CellType) -> object:
    # Safely extract cell contents without blowing up the entire tuple hash
    try:
        return _get_closure_content(content.cell_contents)
    except ValueError:
        return None

