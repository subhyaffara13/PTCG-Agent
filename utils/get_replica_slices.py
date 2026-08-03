import logging
from typing import Optional
import math


def get_replica_slices(
    arr: jax.Array,
    replica_id: Optional[int],
    use_replica_parallel: bool,
    min_slice_bytes_for_replica_parallel: Optional[int] = None,
    max_replicas_for_replica_parallel: Optional[int] = None,
) -> ReplicaSlices:
  """Returns the replica slices a given replica is responsible for.

  Does not transfer allocate or transfer any data.

  Args:
    arr: The jax.Array to get replica slices for.
    replica_id: Configured replica_id. Omitting the replica id just picks the
      first addressable shard's replica id so that the process writes each of
      its addressable shards exactly once. (This is the desired behavior for
      local checkpointing.)
    use_replica_parallel: Whether to use replica-parallel serialization to allow
      arrays with replicated shards to be written cooperatively by different
      hosts.
    min_slice_bytes_for_replica_parallel: Minimum number of bytes per replica
      slice. Only uses replica-parallel when the amount of data written per
      replica is greater than or equal to this number.
    max_replicas_for_replica_parallel: Maximum number of replicas over which
      saving will be parallelized if use_replica_parallel is True.

  Returns:
    ReplicaSlices object.
  """
  Result = tuple[list[ReplicaSlice], Shape]
  shard0 = arr.addressable_shards[0]

  # single-replica: a single replica saves an entire shard.
  def pick_single_replica() -> Result:
    target_replica_id = shard0.replica_id if replica_id is None else replica_id
    rslices = [
        ReplicaSlice(
            index=shard.index,
            unsliced_data=shard.data,
            slice_args=None,
        )
        for shard in arr.addressable_shards
        if shard.replica_id == target_replica_id
    ]
    local_shape = shard0.data.shape
    return rslices, local_shape

  # replica-parallel: every replica saves part of a shard.
  # Logic based on axlearn:
  # https://github.com/apple/axlearn/blob/226d27ab7569668f2c38a35cf32d5dc5190ebdbb/axlearn/common/array_serialization.py#L75
  # TODO(gspschmid): Support replica-parallel in arrays without any evenly-
  # divisible dimension. The last replica would transfer a smaller slice.
  def maybe_pick_replica_parallel() -> Optional[Result]:
    if replica_id is None:
      raise ValueError(
          '`use_replica_parallel` is incompatible with local checkpointing'
      )

    # Check whether replica-parallel applies: we are dealing with non-empty
    # shards, we have more than one replica, and some dimension of the shards
    # is evenly divisible across replicas.
    axis, local_shape, replica_count = (
        calculate_replica_parallel_axis_and_local_shape(
            arr, max_replicas_for_replica_parallel
        )
    )
    if axis is None or local_shape is None or replica_count is None:
      return None

    min_slice_bytes = min_slice_bytes_for_replica_parallel or 0
    if math.prod(local_shape) * arr.itemsize < min_slice_bytes:
      return None

    rslices: list[ReplicaSlice] = []
    for shard in arr.addressable_shards:
      # Sanity check that all shards have the same shape.
      assert shard.data.shape == shard0.data.shape

      # Parallelize saving across only `replica_count` replicas.
      if shard.replica_id >= replica_count:
        continue

      size = local_shape[axis]
      slize = shard.index[axis]
      start = slize.start or 0
      assert slize.step is None
      assert slize.stop is None or slize.stop == start + shard.data.shape[axis]

      start_offset = shard.replica_id * size
      end_offset = start_offset + size
      new_slice = slice(start + start_offset, start + end_offset)

      rslices.append(
          ReplicaSlice(
              index=shard.index[:axis] + (new_slice,) + shard.index[axis + 1 :],
              unsliced_data=shard.data,
              slice_args=SliceArgs(start_offset, end_offset, axis),
          )
      )

    return rslices, local_shape

  if logging.vlog_is_on(1):
    logging.vlog(
        1,
        '[process=%d] get_replica_slices: replica_id=%s, shards=[%s]',
        multihost.process_index(),
        replica_id,  # note: may be None
        ', '.join([
            f'Shard(index={shard.index}, replica_id={shard.replica_id})'
            for shard in arr.addressable_shards
        ]),
    )

  # Small pinned host arrays have layout requirements so slicing them might hang
  # this is a temporary workaround to avoid this. TODO: b/417243451
  is_safe_to_slice = (
      arr.sharding.memory_kind != 'pinned_host'
      or arr.ndim >= 2
      and arr.addressable_shards[0].data.size % 1024 == 0
      and arr.addressable_shards[0].data.shape[-1] % 128 == 0
  )
  # In order for all processes to agree on the right serialization metadata
  # we want to compute the correct local shape regardless of whether there
  # are any replica slices to save locally.
  candidate_slices = None
  if use_replica_parallel and is_safe_to_slice:
    candidate_slices = maybe_pick_replica_parallel()
  if candidate_slices is None:
    candidate_slices = pick_single_replica()  # pytype: disable=attribute-error
  rslices, local_shape = candidate_slices

  if multihost.process_index() == 0:
    # record sharded and replicated arrays metrics
    replica_count = _sharding_num_replicas(arr.sharding, arr.shape)
    if replica_count > 1:
      jax.monitoring.record_scalar(
          '/jax/orbax/write/replicated_array_gb',
          value=np.prod(arr.shape) * arr.dtype.itemsize / (1024**3),
      )
    else:
      jax.monitoring.record_scalar(
          '/jax/orbax/write/sharded_array_gb',
          value=np.prod(arr.shape) * arr.dtype.itemsize / (1024**3),
      )

  return ReplicaSlices(
      global_shape=arr.shape,
      local_shape=local_shape,
      sharding=arr.sharding,
      dtype=arr.dtype,
      is_on_host=False,
      replica_slices=rslices,
  )

