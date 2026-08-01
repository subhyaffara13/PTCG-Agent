
def save_only_these_names(*names_which_can_be_saved):
  """Save only named values, and only among the names given."""
  return SaveOnlyTheseNames(frozenset(names_which_can_be_saved))

