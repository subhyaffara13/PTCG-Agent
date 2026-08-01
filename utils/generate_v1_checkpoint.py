
def generate_v1_checkpoint(path: epath.Path) -> None:
  """Saves a V1 composite checkpoint using save_checkpointables."""
  checkpointables = {
      'state': create_pytree(),
      'metadata': create_json_object(),
  }
  if _OVERWRITE.value:
    path.rmtree(missing_ok=True)

  registry = registration.local_registry()
  registry.add(ocp.handlers.PyTreeHandler, checkpointable_name='state')
  registry.add(ocp.handlers.JsonHandler, checkpointable_name='metadata')
  ctx = ocp.Context()
  ctx.checkpointables.registry = registry
  with ctx:
    ocp.save_checkpointables(
        path,
        checkpointables,
        custom_metadata={'custom': 'meta'},
    )
    (path / 'descriptor').rmtree()  # GOOGLE_INTERNAL

