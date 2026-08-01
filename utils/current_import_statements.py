
def current_import_statements(lazy_modules: dict[str, LazyModule]) -> str:
  """Returns the lazy import statement string."""
  lines = []

  lazy_modules = [m._etils_state for m in lazy_modules.values()]  # pylint: disable=protected-access
  used_lazy_modules = [
      # For convenience, we do not add the `lazy_imports` import
      m
      for m in lazy_modules
      if m.module_loaded and m.alias != 'lazy_imports'
  ]
  std_modules = [m.import_statement for m in used_lazy_modules if m.is_std]
  non_std_modules = [
      m.import_statement for m in used_lazy_modules if not m.is_std
  ]

  # Import standard python module first, then other modules
  lines.extend(std_modules)
  if std_modules and non_std_modules:
    lines.append('')  # Empty line
  lines.extend(non_std_modules)  # pylint: disable=protected-access
  return '\n'.join(lines)

