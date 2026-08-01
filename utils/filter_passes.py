
def filter_passes(regex: str) -> Sequence[Pass]:
  """Gets all registered passes whose display name matches the given regex."""
  return [
      pass_
      for pass_ in _pass_registry.values()
      if re.match(regex, pass_.name)
  ]

