import os

def _get_version_for_build() -> str:
  """Determine the version at build time.

  The returned version string depends on which environment variables are set:
  - if WHEEL_VERSION_SUFFIX is set: version looks like "0.5.1.dev20230906+ge58560fdc"
    Here the WHEEL_VERSION_SUFFIX value is ".dev20230906+ge58560fdc".
    Please note that the WHEEL_VERSION_SUFFIX value is not the same as the
    JAX_CUSTOM_VERSION_SUFFIX value, and WHEEL_VERSION_SUFFIX is set by Bazel
    wheel build rule.
  - if JAX_RELEASE or JAXLIB_RELEASE are set: version looks like "0.4.16"
  - if JAX_NIGHTLY or JAXLIB_NIGHTLY are set: version looks like "0.4.16.dev20230906"
  - if none are set: version looks like "0.4.16.dev20230906+ge58560fdc
  """
  if _release_version is not None:
    return _release_version
  if os.getenv("WHEEL_VERSION_SUFFIX"):
    return _version + os.getenv("WHEEL_VERSION_SUFFIX", "")
  if os.getenv("JAX_RELEASE") or os.getenv("JAXLIB_RELEASE"):
    return _version
  if os.getenv("JAX_NIGHTLY") or os.getenv("JAXLIB_NIGHTLY"):
    return _version_from_todays_date(_version)
  return _version_from_git_tree(_version) or _version_from_todays_date(_version)


def _get_version_for_build() -> str:
  """Determine the version at build time.

  The returned version string depends on which environment variables are set:
  - if WHEEL_VERSION_SUFFIX is set: version looks like "0.5.1.dev20230906+ge58560fdc"
    Here the WHEEL_VERSION_SUFFIX value is ".dev20230906+ge58560fdc".
    Please note that the WHEEL_VERSION_SUFFIX value is not the same as the
    JAX_CUSTOM_VERSION_SUFFIX value, and WHEEL_VERSION_SUFFIX is set by Bazel
    wheel build rule.
  - if JAX_RELEASE or JAXLIB_RELEASE are set: version looks like "0.4.16"
  - if JAX_NIGHTLY or JAXLIB_NIGHTLY are set: version looks like "0.4.16.dev20230906"
  - if none are set: version looks like "0.4.16.dev20230906+ge58560fdc
  """
  if _release_version is not None:
    return _release_version
  if os.getenv("WHEEL_VERSION_SUFFIX"):
    return _version + os.getenv("WHEEL_VERSION_SUFFIX", "")
  if os.getenv("JAX_RELEASE") or os.getenv("JAXLIB_RELEASE"):
    return _version
  if os.getenv("JAX_NIGHTLY") or os.getenv("JAXLIB_NIGHTLY"):
    return _version_from_todays_date(_version)
  return _version_from_git_tree(_version) or _version_from_todays_date(_version)

