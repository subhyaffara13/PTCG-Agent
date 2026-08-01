
def stablehlo_version_at_least(required_version: str) -> bool:
  plugin_version = xla_bridge.backend_stablehlo_version()
  if plugin_version is None:
    return True
  return hlo.get_smaller_version(
      ".".join(map(str, plugin_version)), required_version
  ) == plugin_version

