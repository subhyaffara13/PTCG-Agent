
def _get_version_string() -> str:
  # The build/source distribution for jax & jaxlib overwrites _release_version.
  # In this case we return it directly.
  if _release_version is not None:
    return _release_version
  if os.getenv("WHEEL_VERSION_SUFFIX"):
    return _version + os.getenv("WHEEL_VERSION_SUFFIX", "")
  return _version_from_git_tree(_version) or _version_from_todays_date(_version)


def _get_version_string() -> str:
  # The build/source distribution for jax & jaxlib overwrites _release_version.
  # In this case we return it directly.
  if _release_version is not None:
    return _release_version
  if os.getenv("WHEEL_VERSION_SUFFIX"):
    return _version + os.getenv("WHEEL_VERSION_SUFFIX", "")
  return _version_from_git_tree(_version) or _version_from_todays_date(_version)

