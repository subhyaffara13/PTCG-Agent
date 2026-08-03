from typing import List

def adjacent_positions(position: int, columns: int, rows: int) -> List[int]:
    return [translate(position, action, columns, rows) for action in Action]

