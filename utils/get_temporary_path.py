
def get_temporary_path(
    path: path_types.Path,
    *,
    context: context_lib.Context,
    snapshot_type: snapshot_lib.SnapshotType | None = None,
) -> atomicity_types.TemporaryPath:
  """Gets a :py:class:`~.atomicity_types.TemporaryPath` for the given path.

  Args:
    path: The final path to use for the checkpoint.
    context: The Orbax context.
    snapshot_type: The type of snapshot to use for the temporary path.

  Returns:
    A TemporaryPath for the given path.
  """
  temporary_path_cls = atomicity_defaults.get_default_temporary_path_class(
      path
  )
  tmpdir = temporary_path_cls.from_final(
      path,
      # Ensure metadata store is NOT passed, to prevent separate metadata
      # writing.
      checkpoint_metadata_store=None,
      file_options=context.file_options.v0(),
      snapshot_type=snapshot_type,
  )
  return tmpdir

