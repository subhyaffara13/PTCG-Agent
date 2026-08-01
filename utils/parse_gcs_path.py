
def parse_gcs_path(path: epath.PathLike) -> tuple[str, str]:
  parsed = parse.urlparse(str(path))
  assert parsed.scheme == 'gs', f'Unsupported scheme for GCS: {parsed.scheme}'
  # Strip the leading slash from the path.
  standardized_path = parsed.path
  if standardized_path.startswith('/'):
    standardized_path = standardized_path[1:]
  # Add a trailing slash if it's missing.
  if not standardized_path.endswith('/'):
    standardized_path = standardized_path + '/'
  return parsed.netloc, standardized_path

