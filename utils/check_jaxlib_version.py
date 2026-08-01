
def check_jaxlib_version(jax_version: str, jaxlib_version: str,
                         minimum_jaxlib_version: str) -> tuple[int, ...]:
  # Regex to match a dotted version prefix 0.1.23.456.789 of a PEP440 version.
  # PEP440 allows a number of non-numeric suffixes, which we allow also.
  # We currently do not allow an epoch.
  version_regex = re.compile(r"[0-9]+(?:\.[0-9]+)*")
  def _parse_version(v: str) -> tuple[int, ...]:
    m = version_regex.match(v)
    if m is None:
      raise ValueError(f"Unable to parse jaxlib version '{v}'")
    return tuple(int(x) for x in m.group(0).split('.'))

  _jax_version = _parse_version(jax_version)
  _minimum_jaxlib_version = _parse_version(minimum_jaxlib_version)
  _jaxlib_version = _parse_version(jaxlib_version)

  if _jaxlib_version < _minimum_jaxlib_version:
    msg = (f'jaxlib is version {jaxlib_version}, but this version '
           f'of jax requires version >= {minimum_jaxlib_version}.')
    raise RuntimeError(msg)

  if _jaxlib_version > _jax_version:
    raise RuntimeError(
        f'jaxlib version {jaxlib_version} is newer than and '
        f'incompatible with jax version {jax_version}. Please '
        'update your jax and/or jaxlib packages.')
  return _jaxlib_version

