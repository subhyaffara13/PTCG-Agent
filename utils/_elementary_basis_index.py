
def _elementary_basis_index(axis: str) -> int:
    if axis == "x":
        return 0
    elif axis == "y":
        return 1
    elif axis == "z":
        return 2
    raise ValueError(f"Expected axis to be from ['x', 'y', 'z'], got {axis}")


def _elementary_basis_index(axis: str) -> int:
  if axis == 'x':
    return 0
  elif axis == 'y':
    return 1
  elif axis == 'z':
    return 2
  raise ValueError(f"Expected axis to be from ['x', 'y', 'z'], got {axis}")

