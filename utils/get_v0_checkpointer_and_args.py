
def get_v0_checkpointer_and_args(
    checkpointables: dict[str, Checkpointable],
    *,
    metrics: tree_types.JsonType | None = None,
) -> tuple[
    async_checkpointer.AsyncCheckpointer,
    composite_checkpoint_handler.CompositeArgs,
]:
  """Constructs V0 Checkpointer and Args for saving.

  Args:
    checkpointables: A dictionary of checkpointables.
    metrics: Optional metrics to add to the checkpointables.

  Returns:
    A tuple containing the V0 Checkpointer and Args.
  """
  context = context_lib.get_context()
  checkpointables = execution.add_internal_checkpointables(
      checkpointables, context=context, metrics=metrics
  )

  handlers = {
      name: handler_registration.resolve_handler_for_save(
          context.checkpointables_options.registry, checkpointable, name=name
      )
      for name, checkpointable in checkpointables.items()
  }
  compatibility_handlers = {
      name: handler_compatibility.get_compatibility_handler(handler)
      for name, handler in handlers.items()
  }
  handler_registry = (
      legacy_handler_registration.DefaultCheckpointHandlerRegistry()
  )
  for name, handler in compatibility_handlers.items():
    handler_registry.add(name, handler_compatibility.Args, handler)
  composite_options = composite_checkpoint_handler.CompositeOptions(
      async_options=context.async_options.v0(),
      file_options=context.file_options.v0(),
      multiprocessing_options=context.multiprocessing_options.v0(),
  )
  ckptr = async_checkpointer.AsyncCheckpointer(
      composite_checkpoint_handler.CompositeCheckpointHandler(
          handler_registry=handler_registry,
          composite_options=composite_options,
      ),
      async_options=context.async_options.v0(),
      multiprocessing_options=context.multiprocessing_options.v0(),
      file_options=context.file_options.v0(),
  )
  args = composite_checkpoint_handler.CompositeArgs(**{
      name: handler_compatibility.Args(checkpointable)
      for name, checkpointable in checkpointables.items()
  })
  return ckptr, args

