
def _map_rows(block):
    """Parse a CSV-style map block into a 2D list of tile-code strings."""
    return [[cell.strip() for cell in line.split(",")] for line in block.strip().splitlines()]

