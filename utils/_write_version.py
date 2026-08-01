
def _write_version(fname: str) -> None:
  """Used by setup.py to write the specified version info into the source tree."""
  release_version = _get_version_for_build()
  old_version_string = "_release_version: str = '0.10.2'"
  new_version_string = f"_release_version: str = {release_version!r}"
  fhandle = pathlib.Path(fname)
  contents = fhandle.read_text()
  # Expect two occurrences: one above, and one here.
  if contents.count(old_version_string) != 2:
    raise RuntimeError(f"Build: could not find {old_version_string!r} in {fname}")
  contents = contents.replace(old_version_string, new_version_string)

  githash = os.environ.get("JAX_GIT_HASH")
  if githash:
    old_githash_string = "_git_hash: str = '990e6a0b84138346e6a38785412f36356e0e5dc3'"
    new_githash_string = f"_git_hash: str = {githash!r}"
    if contents.count(old_githash_string) != 2:
      raise RuntimeError(f"Build: could not find {old_githash_string!r} in {fname}")
    contents = contents.replace(old_githash_string, new_githash_string)
  fhandle.write_text(contents)


def _write_version(fname: str) -> None:
  """Used by setup.py to write the specified version info into the source tree."""
  release_version = _get_version_for_build()
  old_version_string = "_release_version: str = '0.10.2'"
  new_version_string = f"_release_version: str = {release_version!r}"
  fhandle = pathlib.Path(fname)
  contents = fhandle.read_text()
  # Expect two occurrences: one above, and one here.
  if contents.count(old_version_string) != 2:
    raise RuntimeError(f"Build: could not find {old_version_string!r} in {fname}")
  contents = contents.replace(old_version_string, new_version_string)

  githash = os.environ.get("JAX_GIT_HASH")
  if githash:
    old_githash_string = "_git_hash: str = '990e6a0b84138346e6a38785412f36356e0e5dc3'"
    new_githash_string = f"_git_hash: str = {githash!r}"
    if contents.count(old_githash_string) != 2:
      raise RuntimeError(f"Build: could not find {old_githash_string!r} in {fname}")
    contents = contents.replace(old_githash_string, new_githash_string)
  fhandle.write_text(contents)

