
def load_async(
    path: path_types.PathLike,
    abstract_state: (
        AbstractPyTree | CheckpointMetadata[AbstractPyTree] | None
    ) = None,
    *,
    checkpointable_name: str | None = STATE_CHECKPOINTABLE_KEY,
) -> async_types.AsyncResponse[tree_types.PyTreeOf[tree_types.Leaf]]:
  """Loads a PyTree asynchronously. Currently has limited support."""
  start_time = time.time()
  event_tracking.OperationRecorder(
      path,
      operation_type=event_tracking.OperationType.LOAD,
      async_origin=True,
  ).record_start(start_time)
  ctx = context_lib.get_context()
  # Ensure the operation ID is incremented as soon as possible. This must be
  # done uniquely for each load operation.
  asyncio_utils.run_sync(
      synchronization.synchronize_next_operation_id(
          prefix=ctx.multiprocessing_options.barrier_sync_key_prefix,
          processes=ctx.multiprocessing_options.active_processes,
      )
  )
  if not path:
    raise ValueError('Path must not be None.')
  if ctx.checkpoint_layout != options_lib.CheckpointLayout.SAFETENSORS:
    raise NotImplementedError(
        'Asynchronous loading only supported for SAFETENSORS checkpoint '
        f'layout, not {ctx.checkpoint_layout}.'
    )
  path = ctx.file_options.path_class(path)
  abstract_state = _standardize_abstract_checkpointables(abstract_state)
  validation.validate_state_checkpointable_name(checkpointable_name)
  validation.validate_abstract_state(abstract_state)

  async def _blocking_load() -> Any:
    resolver = await layout_registry.CheckpointLayoutResolver.resolve(
        path, ctx.checkpoint_layout, pytree_name=checkpointable_name
    )
    return await resolver.layout.load(
        path,
        checkpointable_name=resolver.pytree_name,
        abstract_state=abstract_state,
    )

  background_awaitable = asyncio_utils.run_sync(_blocking_load())
  response = _LoadPyTreeResponse.create(
      background_awaitable,
      path,
      start_time=start_time,
      context=ctx,
  )
  return response

