
def _set_up_destination(root: str | PathLike[str], overwrite: bool,
                        pytree_repr: dict[str, Any], distinct_locations: bool,
                        sync_key: str | None) -> dict[str, Any]:
  """Inspect the destination, set it up for writing, potentially read existing data."""
  root = _norm_path(root)
  if overwrite:
    if root.exists() and len(list(root.iterdir())) > 0:
      # check that we're only deleting things that come from JAX
      # refuse to rm directories containing additional entries
      extra_member_paths = [
          path for path in list(root.iterdir()) if path.name not in
          (_PYTREEDEF_FILE, _ARCHIVE_NAME, _ARRAY_STORE_DIRNAME)]

      if len(extra_member_paths) != 0:
        raise RuntimeError(
            "Refusing to work on a directory that is not a previous checkpoint."
            f" Unrecognized paths: {extra_member_paths}. Remove them manually"
            f" if you're sure you want to use {root} as the checkpoint"
            " directory.")

      if (jax.process_index() == 0 or distinct_locations) and root.exists():
        _rm_dir(root)
    _sync_on_key(sync_key, "overwrite")
    return pytree_repr
  else:
    if (root.exists() and len(list(root.iterdir())) > 0):  # not empty
      raise ValueError(f"Files already exist at path: `{root}`, but you"
                       f" specified `{overwrite=}`")
    return pytree_repr

