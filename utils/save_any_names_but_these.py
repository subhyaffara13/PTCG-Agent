
def save_any_names_but_these(*names_not_to_save):
  """Save only named values, i.e. any outputs of `checkpoint_name`, excluding
  the names given."""
  return SaveAnyNamesButThese(frozenset(names_not_to_save))

