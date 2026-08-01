
def print_current_imports() -> None:
  """Display the active lazy imports.

  This can be used before publishing a colab. To convert lazy imports
  into explicit imports.

  For convenience, `from etils.ecolab import lazy_imports` is excluded from
  the current imports.
  """
  print(lazy_utils.current_import_statements(LAZY_MODULES))

