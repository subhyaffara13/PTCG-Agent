
def _generate_fixture(config_file: str, output_directory: str) -> None:
  """Generates the synthetic checkpoint described by a config, then returns.

  Builds the data from the config's `checkpoint_config` spec on the config's
  mesh and writes it with `ocp.save`. The plumbing stops at this entrypoint:
  the benchmark classes are never involved in fixture generation.

  Args:
    config_file: Path to the YAML config whose `checkpoint_config` supplies the
      spec and whose `mesh_config` supplies the mesh.
    output_directory: Directory to write the generated Orbax checkpoint to.
  """
  checkpoint_configs, mesh_configs = config_parsing.parse_config(config_file)
  mesh = device_mesh.create_mesh(mesh_configs[0]) if mesh_configs else None
  checkpoint_generation.generate_and_save_checkpoint(
      checkpoint_configs[0], output_directory, mesh=mesh
  )

