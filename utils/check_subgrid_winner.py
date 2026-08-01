
def check_subgrid_winner(subgrid: list[str]) -> str:
    """Check if a 3x3 sub-grid has a winner or is a draw."""
    lines = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],  # rows
        [0, 3, 6],
        [1, 4, 7],
        [2, 5, 8],  # cols
        [0, 4, 8],
        [2, 4, 6],  # diagonals
    ]
    for line in lines:
        if subgrid[line[0]] != "" and subgrid[line[0]] == subgrid[line[1]] == subgrid[line[2]]:
            return subgrid[line[0]]
    if all(cell != "" for cell in subgrid):
        return "draw"
    return ""

