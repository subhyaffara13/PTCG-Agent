import re

def check_plugin_version(
    plugin_name: str, jaxlib_version: str, plugin_version: str
) -> bool:
  """Check if a plugin version is compatible with the jaxlib version.

  Args:
    plugin_name: Name of the plugin module.
    jaxlib_version: The installed jaxlib version string.
    plugin_version: The installed plugin version string.

  Returns:
    True if the plugin is compatible, False otherwise.
  """
  # ROCm plugins skip runtime version checks. Version compatibility is managed
  # via pip dependency constraints in setup.py instead. This allows ROCm plugins
  # to be released on their own schedule without strict jaxlib version coupling.
  is_rocm_plugin = any(
      rocm_name in plugin_name
      for rocm_name in _PLUGIN_MODULE_NAMES.get("rocm", [])
  )
  if is_rocm_plugin:
    return True

  # Regex to match a dotted version prefix 0.1.23.456.789 of a PEP440 version.
  # PEP440 allows a number of non-numeric suffixes, which we allow also.
  # We currently do not allow an epoch.
  version_regex = re.compile(r"[0-9]+(?:\.[0-9]+)*")

  def _parse_version(v: str) -> tuple[int, ...]:
    m = version_regex.match(v)
    if m is None:
      raise ValueError(f"Unable to parse version string '{v}'")
    return tuple(int(x) for x in m.group(0).split("."))

  if _parse_version(jaxlib_version) != _parse_version(plugin_version):
    warnings.warn(
        f"JAX plugin {plugin_name} version {plugin_version} is installed, but "
        "it is not compatible with the installed jaxlib version "
        f"{jaxlib_version}, so it will not be used.",
        RuntimeWarning,
    )
    return False
  return True

