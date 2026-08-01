
def clear_cached_modules(
    modules: py_utils.StrOrStrList,
    *,
    recursive: bool = True,
    verbose: bool = False,
    invalidate: bool = True,
) -> None:
  """Clear the `sys.modules` cache.

  Helpful for interactive development to reload from Jupyter notebook the
  code we're currently editing (without having to restart the notebook kernel).

  Usage:

  ```python
  ecolab.clear_cached_modules(['visu3d', 'other_module.submodule'])

  import visu3d
  import other_module.submodule
  ```

  Args:
    modules: List of modules to clear
    recursive: Whether submodules are cleared too
    verbose: Whether to display the list of modules cleared.
    invalidate: If `True` (default), the instances of the module will raise an
      error when used (to avoid using 2 versions of a module at the same time)
  """
  modules_to_clear = get_module_names(modules, recursive=recursive)
  if not modules_to_clear:
    return

  modules = set(py_utils.normalize_str_to_list(modules))

  for module_name in modules_to_clear:
    if verbose:
      print(f'Clearing {module_name}')

    # We do not invalidate ecolab
    # Note that `reload=['etils']` will still clear `ecolab` from `sys.modules`
    # even if it is not reloaded. In practice, this is fine as `ecolab`
    # should only be imported once in the colab.
    invalidate_curr = invalidate and not module_name.startswith('etils')

    # Only the top-most attribute should be cleared. when `invalidate=False`
    # Otherwise, childs are not re-imported
    # Clear the parent ref to the module
    if invalidate_curr or module_name in modules:
      _clear_parent_module_attr(module_name)

    if invalidate_curr:
      # Mutate the existing modules to raise an error if accessed
      _invalidate_module(sys.modules[module_name])

    del sys.modules[module_name]

  # The typing module has side effect by caching `A[B]` from the old modules
  # but thankfully they expose the cleanup method.
  for cleanup in typing._cleanups:  # pytype: disable=module-attr  # pylint: disable=protected-access
    cleanup()

