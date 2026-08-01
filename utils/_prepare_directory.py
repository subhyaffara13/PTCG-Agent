
def _prepare_directory(root: str | PathLike[str], overwrite: bool,
                       pytreedef_repr: dict[str, Any], distinct_locations: bool,
                       sync_key: str | None):
  """Prepare the directory: check destination, potentially read existing data
  and overwrite.

  Raises:
    RuntimeError: If the destination directory cannot be created.
  """
  root = _norm_path(root)
  # prepare the destination directory, overwrite destination directory or error
  pytreedef_repr = _set_up_destination(
      root, overwrite, pytreedef_repr, distinct_locations, sync_key)

  if not _is_remote_path(root) and (distinct_locations
                                    or jax.process_index() == 0):
    root.mkdir(exist_ok=True)  # do not make parents, that's too much
    if not root.exists() or not root.is_dir():
      raise RuntimeError(f"Could not create destination directory at {root}")
  _sync_on_key(sync_key, "mkdir")
  return pytreedef_repr

