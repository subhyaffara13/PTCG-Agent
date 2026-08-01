
def _is_orbax_checkpoint(path: str) -> bool:
  return (
      io.exists(os.path.join(path, ORBAX_CKPT_FILENAME))
      or io.exists(os.path.join(path, ORBAX_METADATA_FILENAME))
      or io.exists(os.path.join(path, ORBAX_MANIFEST_OCDBT))
  )

