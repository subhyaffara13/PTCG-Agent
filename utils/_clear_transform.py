
def _clear_transform(list_):
  # Support `ecolab` adhoc `reload`
  for elem in list(list_):
    if hasattr(elem, '__is_ecolab__'):
      list_.remove(elem)

