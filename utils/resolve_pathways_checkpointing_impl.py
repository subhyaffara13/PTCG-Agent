
def resolve_pathways_checkpointing_impl(
    context: context_lib.Context,
) -> pathways_types.CheckpointingImpl:
  """Returns the Pathways checkpointing implementation."""
  checkpointing_impl = context.pathways_options.checkpointing_impl
  return checkpointing_impl or pathways_types.CheckpointingImpl.from_options(
      use_colocated_python=False,  # Not enabled unless explicitly requested.
      use_persistence_array_handler=True,  # Only used as a fallback.
  )

