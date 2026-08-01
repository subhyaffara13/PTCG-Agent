
def _init_dims(shape: tuple[int, ...], t1: int, t2: int) -> list[list[Factor]]:
  dims: list[list[Factor]] = []
  for i, s in enumerate(shape):
    if i == len(shape) - 2:
      kind, t_size = "sublane", t1
    elif i == len(shape) - 1:
      kind, t_size = "lane", t2
    else:
      kind, t_size = "outer", 1

    current_dim = []
    assert s % t_size == 0
    if s // t_size > 1:
      current_dim.append(Factor(s // t_size, "outer"))
    if t_size > 1 or kind != "outer":
      current_dim.append(Factor(t_size, kind))
    dims.append(_consolidate(current_dim))
  return dims

