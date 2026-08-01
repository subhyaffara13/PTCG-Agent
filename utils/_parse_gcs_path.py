
def _parse_gcs_path(gcs_path: str) -> tuple[str, str]:
  """Parses a GCS path like gs://bucket/prefix/file into (bucket, prefix)."""
  path_no_scheme = gcs_path.replace("gs://", "")
  parts = path_no_scheme.split("/", 1)
  bucket = parts[0]
  prefix = parts[1] if len(parts) > 1 else ""
  return bucket, prefix

