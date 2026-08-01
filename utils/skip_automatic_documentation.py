
def skip_automatic_documentation(obj: Any):
  """Marks an object as skipped for automatic documentation generation."""
  _SKIPPED_FOR_AUTODOC[id(obj)] = obj
  return obj

