
def is_standard_name_format(name_format: NameFormat[Metadata]) -> bool:
  """Returns True if the name format is a standard name format."""
  return isinstance(name_format, _StandardNameFormat)

