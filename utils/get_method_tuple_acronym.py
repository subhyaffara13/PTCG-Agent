
def get_method_tuple_acronym(method_tuple):
  """Returns pretty acronym for specified ResponseGraphUCB method tuple."""
  if isinstance(method_tuple, tuple):
    acronyms = [get_method_acronym(m) for m in method_tuple]
    return ', '.join(acronyms)
  else:
    return get_method_acronym(method_tuple)

