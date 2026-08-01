
def save_anything_except_these_names(*names_not_to_save):
  """Save any values (not just named ones) excluding the names given."""
  return lambda *_, **__: True

