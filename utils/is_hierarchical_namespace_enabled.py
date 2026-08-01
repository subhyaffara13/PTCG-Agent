
def is_hierarchical_namespace_enabled(path: epath.PathLike) -> bool:
  """Return whether hierarchical namespace is enabled."""
  parsed = parse.urlparse(str(path))
  if parsed.scheme != 'gs':
    return False
  bucket_name, _ = parse_gcs_path(path)
  bucket = get_bucket(bucket_name)
  return (
      hasattr(bucket, 'hierarchical_namespace_enabled')
      and bucket.hierarchical_namespace_enabled
  )

