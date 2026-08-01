
def setup_test_directory(
    name: str, base_path: str | None = None, repeat_index: int | None = None
) -> epath.Path:
  """Creates a unique, clean test directory for a benchmark run.

  It supports both local filesystems and cloud storage (like GCS) via etils.

  Args:
      name: The name of the test, used to create the directory.
      base_path: The parent directory. Defaults to /tmp/orbax_benchmarks/.
      repeat_index: If provided, a subdirectory for the repetition is created.

  Returns:
      A path pointing to the created directory.
  """
  base_path = "/tmp/orbax_benchmarks" if base_path is None else base_path
  path = epath.Path(base_path) / name
  if repeat_index is not None:
    path = path / f"repeat_{repeat_index}"
  logging.info("Setting up test directory at: %s", path)
  if multihost.get_process_index() == 0:
    if path.exists() and not base_path.startswith("gs://"):
      logging.warning("Test directory %s already exists. Deleting it.", path)
      path.rmtree()
    path.mkdir(parents=True, exist_ok=True)
  return path

