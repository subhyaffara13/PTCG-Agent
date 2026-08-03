from typing import Any

def get_leaf_types(hint: TypeForm) -> list[type[Any]]:
  """Extract the inner list of the types (`Optional[A] -> [A, None]`)."""
  all_types = []

  def _collect_leaf_types(hint):
    all_types.append(hint)

  visit(hint, leaf_fn=_collect_leaf_types)

  return all_types

