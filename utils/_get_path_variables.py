
def _get_path_variables(
  path: tuple[str, ...], variables: FrozenVariableDict
) -> MutableVariableDict:
  """A function that takes a path and a variables structure and returns the
  variable structure at that path.
  """
  path_variables = {}

  for collection in variables:
    collection_variables = variables[collection]
    for name in path:
      if name not in collection_variables:
        collection_variables = None
        break
      collection_variables = collection_variables[name]

    if collection_variables is not None:
      path_variables[collection] = unfreeze(collection_variables)

  return path_variables

