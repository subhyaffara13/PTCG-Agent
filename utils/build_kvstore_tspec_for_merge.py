
def build_kvstore_tspec_for_merge(
    directory: str,
    subdir: str,
) -> JsonSpec:
  """Constructs a spec for a Tensorstore KvStore."""

  tokens = subdir.split('_')
  process_id = tokens[-1]
  is_replica_separate_folder = REPLICA_SUBDIR_SUFFIX in subdir
  return build_kvstore_tspec(
      directory,
      use_ocdbt=True,
      process_id=process_id,
      replica_separate_folder=is_replica_separate_folder,
  )

