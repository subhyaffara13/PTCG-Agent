
def ensure_atomic_save(
    temp_ckpt_dir: epath.Path,
    final_ckpt_dir: epath.Path,
    metadata_store: Optional[checkpoint_metadata.MetadataStore] = None,
):
  """Wrapper around TemporaryPath.finalize for testing."""
  if temp_ckpt_dir == final_ckpt_dir:
    asyncio_utils.run_sync(
        atomicity.CommitFileTemporaryPath(
            temp_ckpt_dir,
            final_ckpt_dir,
            checkpoint_metadata_store=metadata_store,
        ).finalize(
        )
    )
  else:
    asyncio_utils.run_sync(
        atomicity.AtomicRenameTemporaryPath(
            temp_ckpt_dir,
            final_ckpt_dir,
            checkpoint_metadata_store=metadata_store,
        ).finalize(
        )
    )

