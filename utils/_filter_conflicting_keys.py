import itertools
from typing import Any

def _filter_conflicting_keys(d: dict[str, Any]) -> dict[str, Any]:
  """Filters metadata keys that conflict due to parent-child relationships.

  When merging metadata from multiple partial saves, we might encounter
  conflicting entries. For example, one partial save might save 'a/b' as a
  leaf, while another saves 'a/b/c' as a leaf. This is a conflict because
  'a/b' cannot be both a leaf and an intermediate node containing 'c'. This
  function resolves the conflict by removing metadata for 'a/b', keeping
  'a/b/c', and implicitly treating 'a/b' as an intermediate node.

  Args:
    d: A dictionary of metadata.

  Returns:
    The filtered metadata dictionary.
  """
  keys = list(d.keys())
  to_remove = set()

  parsed_keys = {}
  for k in keys:
    try:
      parsed_keys[k] = ast.literal_eval(k)
    except (ValueError, SyntaxError):
      parsed_keys[k] = k

  for k1, k2 in itertools.permutations(keys, 2):
    t1, t2 = parsed_keys[k1], parsed_keys[k2]
    if isinstance(t1, tuple) and isinstance(t2, tuple):
      if _is_prefix(t1, t2):
        to_remove.add(k1)
    elif isinstance(k1, str) and isinstance(k2, str):
      if k2.startswith((k1 + '.', k1 + '/')):
        to_remove.add(k1)

  for k in to_remove:
    del d[k]
  return d

