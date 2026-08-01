
def _unflatten_to_simple_structure(
  xs: list[tuple[tuple[tp.Any, ...], tp.Any]], *, original: tp.Any
):
  """Rebuild a simple Python structure from path/value leaves.

  This variant is aware of the original object so it can:
  - Preserve empty containers that were elided by JAX flattening.
  - Pad trailing missing list/tuple items using the original length.
  - Distinguish placeholders for empty dict/list vs None.
  """

  def _get_by_path(x, path: tuple[tp.Any, ...]):
    cur = x
    for k in path:
      cur = cur[k]
    return cur

  def _to_simple(x):
    # Convert to display-friendly simple structures
    if isinstance(x, (list, tuple)):
      return [_to_simple(e) for e in x]
    if isinstance(x, dict):
      return {k: _to_simple(v) for k, v in x.items()}
    return x

  result: list | dict = (
    [] if len(xs) > 0 and isinstance(xs[0][0][0], int) else {}
  )
  for path, value in xs:
    cursor = result
    for i, key in enumerate(path[:-1]):
      if isinstance(cursor, list):
        # Ensure list has slot for current key; infer placeholder from original
        while len(cursor) <= key:
          # path to the slot we are about to create
          slot_path = path[:i] + (len(cursor),)
          try:
            orig_slot = _get_by_path(original, slot_path)
          except Exception:
            orig_slot = None
          if isinstance(orig_slot, (list, tuple)):
            cursor.append([])
          elif isinstance(orig_slot, dict):
            cursor.append({})
          else:
            cursor.append(None)
      else:
        if key not in cursor:
          next_key = path[i + 1]
          if isinstance(next_key, int):
            cursor[key] = []
          else:
            cursor[key] = {}
      cursor = cursor[key]
    if isinstance(cursor, list):
      # Handle gaps in indices caused by JAX flattening eliding empty containers
      while len(cursor) <= path[-1]:
        slot_path = path[:-1] + (len(cursor),)
        try:
          orig_slot = _get_by_path(original, slot_path)
        except Exception:
          orig_slot = None
        if isinstance(orig_slot, (list, tuple)):
          cursor.append([])
        elif isinstance(orig_slot, dict):
          cursor.append({})
        else:
          cursor.append(None)
      cursor[path[-1]] = value
    else:
      assert isinstance(cursor, dict)
      cursor[path[-1]] = value
  # If original is a sequence and result is a list, pad trailing items
  if isinstance(original, (list, tuple)) and isinstance(result, list):
    for i in range(len(result), len(original)):
      slot = original[i]
      result.append(_to_simple(slot))
  return result

