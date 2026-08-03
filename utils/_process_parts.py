import os

def _process_parts(*parts: PathLike) -> tuple[PathLike, ...]:
  """Supports the `xx://` prefix."""
  full_path = '/'.join(os.fspath(p) for p in parts)
  if full_path.startswith(_URI_PREFIXES):
    prefix, _ = full_path.split('://', maxsplit=1)
    prefix = f'{prefix}://'
    new_prefix = _URI_MAP_ROOT[prefix]
    return (full_path.replace(prefix, new_prefix, 1),)
  else:
    return parts

