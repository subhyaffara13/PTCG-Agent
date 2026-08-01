
def _load_module(
    module_name: str,
    *,
    extra_imports: list[str],
) -> types.ModuleType:
  """Load the module, eventually using adhoc-import."""
  adhoc_cm = contextlib.suppress()

  # First time, load the module
  with adhoc_cm:
    for extra_import in extra_imports:
      # Hardcoded hack to not import tqdm.notebook on non-Colab env
      if extra_import == 'tqdm.notebook' and not epy.is_notebook():
        continue
      importlib.import_module(extra_import)
    return importlib.import_module(module_name)

