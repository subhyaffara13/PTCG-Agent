
def _get_unique_consts(
    consts: Sequence[Sequence[Any]],
) -> tuple[list[Array], set[int]]:
  unique_consts = []
  unique_const_ids = set()
  for cs in consts:
    for c in cs:
      if id(c) not in unique_const_ids:
        unique_consts.append(c)
        unique_const_ids.add(id(c))
  return unique_consts, unique_const_ids

