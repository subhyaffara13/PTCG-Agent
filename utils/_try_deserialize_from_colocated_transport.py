
def _try_deserialize_from_colocated_transport(
    restored_state: PyTree,
    template_state: PyTree,
) -> PyTree | None:
  try:
    return tree_utils.deserialize_tree(restored_state, template_state)
  except (AttributeError, IndexError, KeyError, TypeError, ValueError):
    return None

