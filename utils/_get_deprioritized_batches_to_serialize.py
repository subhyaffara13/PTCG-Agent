import logging

def _get_deprioritized_batches_to_serialize(
    deprioritized_params: Sequence[
        tuple[jax.Array, types.ParamInfo, types.SaveArgs]
    ],
    *,
    device_host_max_bytes: int,
    replica_id: int | None,
    dispatcher: dispatchers.Dispatcher | None,
):
  """Yields batches of info, args, and arrays that fit within the memory budget."""
  logging.info(
      'Option `device_host_max_bytes` was set to %s. Using memory-limited'
      ' saving. Note that this feature may impact saving speed.',
      humanize.naturalsize(device_host_max_bytes, binary=True),
  )
  if deprioritized_params:
    arrays_saved_count = 0
    for batch in worker_memory_utils.next_memory_budgeted_batch(
        deprioritized_params,
        device_host_max_bytes,
        replica_id=replica_id,
        dispatcher=dispatcher,
    ):
      assert arrays_saved_count < len(deprioritized_params)
      logging.info(
          'Scheduling serialization of %d deprioritized arrays. Already'
          ' completed %d / %d arrays. Included keys: %s',
          len(batch),
          arrays_saved_count,
          len(deprioritized_params),
          [tree_utils.str_keypath(info.keypath) for _, info, _ in batch],
      )
      yield zip(*batch)
      logging.info(
          'Serialization of %d deprioritized jax.Array completed.',
          len(batch),
      )
      arrays_saved_count += len(batch)

    assert arrays_saved_count == len(deprioritized_params)

