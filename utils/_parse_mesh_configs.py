
def _parse_mesh_configs(
    config: dict[str, Any],
) -> list[config_lib.MeshConfig] | None:
  """Builds the mesh configs from the YAML, or None if unspecified."""
  if 'mesh_configs' in config:
    return [config_lib.MeshConfig(**mc) for mc in config['mesh_configs']]
  if 'mesh_config' in config:
    return [config_lib.MeshConfig(**config['mesh_config'])]
  return None

