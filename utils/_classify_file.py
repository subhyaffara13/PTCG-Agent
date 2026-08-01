
def _classify_file(name: str) -> str:
  """Buckets a leaf filename into a format category.

  Args:
    name: The leaf filename to classify.

  Returns:
    One of "ocdbt", "zarr3", "metadata", or "other".
  """
  if name.startswith("ocdbt.process_") or name == "manifest.ocdbt":
    return "ocdbt"
  if name in ("zarray", "zgroup", "zarr.json") or name.endswith(".zarr"):
    return "zarr3"
  if name in ("_METADATA", "_sharding", "_CHECKPOINT_METADATA"):
    return "metadata"
  return "other"

