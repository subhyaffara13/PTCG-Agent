
def value_metadata_tree_from_json_str(json_str: str) -> PyTree:
  """Returns a PyTree from the given JSON string."""
  return simplejson.loads(
      json_str,
      object_hook=_value_metadata_tree_for_json_loads,
  )

