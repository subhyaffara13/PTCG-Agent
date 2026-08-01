
def _checkpointer_save_composite_mixed(path: epath.Path) -> None:
  """Saves a composite checkpoint using Checkpointer + CompositeHandler."""
  json_object = create_json_object()
  pytree = create_pytree()
  checkpoint_args = args.Composite(**{
      'state': args.PyTreeSave(pytree),  # Represents pytree checkpointable.
      'metadata': args.JsonSave(json_object),
  })
  if _OVERWRITE.value:
    path.rmtree(missing_ok=True)
  with v0_checkpointer.Checkpointer(
      composite_checkpoint_handler.CompositeCheckpointHandler()
  ) as checkpointer:
    checkpointer.save(path, checkpoint_args, custom_metadata={'custom': 'meta'})

