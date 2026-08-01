
def _get_local_part_index(parts: Sequence[str]) -> int:
  for i, part in enumerate(parts):
    if part.startswith(_LOCAL_PART_PREFIX):
      return i
  raise ValueError(
      f'Did not find a local part ({_LOCAL_PART_PREFIX}) in parts: {parts}'
  )

