
def register_pathways_handlers(
    use_single_replica_array_handler: bool = False,
    checkpointing_impl: CheckpointingImpl | None = None,
    **kwargs,
):
  """Registers the Pathways handlers with the given options.

  Args:
    use_single_replica_array_handler: Whether to use the
      SingleReplicaArrayHandler.
    checkpointing_impl: The implementation to use for Pathways checkpointing.
    **kwargs: Keyword arguments to pass to the ArrayHandler.
  """
  _register_numpy_and_scalar_handlers()

  type_handler_registry.register_type_handler(
      jax.Array,
      get_pathways_array_handler(
          use_single_replica_array_handler,
          checkpointing_impl=checkpointing_impl,
          **kwargs,
      ),
      override=True,
  )

