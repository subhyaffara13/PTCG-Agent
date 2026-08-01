
def next_memory_budgeted_batch(
    params: Sequence[tuple[jax.Array, types.ParamInfo, types.SaveArgs]],
    worker_memory_budget: int,
    *,
    replica_id: int | None,
    dispatcher: dispatchers.Dispatcher | None,
):
  """Yields batches of info, args, and arrays that fit within the memory budget.

  Args:
    params: A sequence of (array, info, args) tuples.
    worker_memory_budget: The maximum amount of memory that can be used on any
      worker.
    replica_id: The replica id to use for estimation. If None, all replicas are
      used.
    dispatcher: The dispatcher instance to use. If None, the default dispatcher
      is used.
  """
  arrays, infos, args = zip(*params, strict=True)
  if dispatcher is None:
    device_to_worker_ids_map = {
        d.id: multihost.process_index_from_device(d) for d in jax.devices()
    }
  else:
    device_to_worker_ids_map = _device_to_worker_ids(dispatcher)
    # NOTE: We only transfer save shards with replica_id == replica_id, but we
    # are actually redundantly transferring all shards, thanks to remote python
    # / colcoated python. So we set replica_id to None, to estimate memory usage
    # for all replicas.
    replica_id = None

  def _no_worker_memory_usage() -> dict[int, int]:
    return {id: 0 for id in set(device_to_worker_ids_map.values())}

  current_batch = [(arrays[0], infos[0], args[0])]
  current_worker_memory_usage = _estimate_worker_memory_usage(
      arrays[0],
      replica_id=replica_id,
      device_to_worker_ids_map=device_to_worker_ids_map,
  )

  for arr, info, arg in zip(arrays[1:], infos[1:], args[1:]):
    incremented_worker_memory_usage = _increment_worker_memory_usage(
        arr,
        current_worker_memory_usage,
        replica_id=replica_id,
        device_to_worker_ids_map=device_to_worker_ids_map,
    )
    if _is_array_under_memory_budget(
        worker_memory_budget, incremented_worker_memory_usage
    ):
      current_batch.append((arr, info, arg))
      current_worker_memory_usage = incremented_worker_memory_usage
    else:
      assert current_batch
      logging.info(
          '[process=%d] Obtained a memory-limited batch (replica_id=%s) with'
          ' %d arrays. Per-worker, projected to cost: %s',
          multihost.process_index(),
          replica_id,
          len(current_batch),
          _humanize_worker_memory_usage(current_worker_memory_usage),
      )
      yield current_batch

      # Assumes arrays have completed saving and worker memory has been freed.
      # The current array still needs to be dealt with.
      current_batch = [(arr, info, arg)]
      current_worker_memory_usage = _increment_worker_memory_usage(
          arr,
          _no_worker_memory_usage(),
          replica_id=replica_id,
          device_to_worker_ids_map=device_to_worker_ids_map,
      )

  if current_batch:
    logging.info(
        '[process=%d] Obtained a memory-limited batch (replica_id=%s) with %d'
        ' arrays. Per-worker, projected to cost: %s',
        multihost.process_index(),
        replica_id,
        len(current_batch),
        _humanize_worker_memory_usage(current_worker_memory_usage),
    )
    yield current_batch

