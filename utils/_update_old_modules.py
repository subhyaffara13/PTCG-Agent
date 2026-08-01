
def _update_old_modules(
    *,
    reload: list[str],
    previous_modules: dict[str, _ModuleRefs],
    verbose: bool,
    recursive: bool,
) -> None:
  """Update all old modules."""
  # Don't spend time updating types that are already dead anyway.
  gc.collect()

  start_time = time.time()

  updater = _ObjectUpdater()

  for module_name in module_utils.get_module_names(reload, recursive=recursive):
    new_module = sys.modules[module_name]
    old_module_refs = previous_modules.get(module_name)
    if old_module_refs is not None:
      previous_modules[module_name] = (
          old_module_refs.update_refs_with_new_module(
              new_module, updater, verbose=verbose
          )
      )

  # Finally update all existing instances to their new class.
  updater.update_instances()

  if verbose:
    print(
        "Inplace reloading old modules took"
        f" {time.time() - start_time:.2} seconds."
    )

