
def _get_grain_shm_array_metadata_cls():
  """Imports the shm metadata from `grain` in a cross-version compatible way."""
  # pylint: disable=g-import-not-at-top  # pytype: disable=import-error
  import grain

  cls = getattr(
      grain.multiprocessing,
      'SharedMemoryArrayMetadata',
      None,
  )
  if cls is None:
    from grain._src.python import shared_memory_array

    cls = shared_memory_array.SharedMemoryArrayMetadata
  # pylint: enable=g-import-not-at-top  # pytype: enable=import-error
  return cls

