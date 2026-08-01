
def _get_replica_slices(
    arrays: Sequence[jax.Array],
    replica_id: int,
    use_replica_parallel: bool,
    min_slice_bytes_for_replica_parallel: int | None = None,
    max_replicas_for_replica_parallel: int | None = None,
) -> Sequence[replica_slices.ReplicaSlices]:
  """Returns ReplicaSlices for arrays."""
  rslices_per_array = [
      replica_slices.get_replica_slices(
          arr,
          replica_id,
          use_replica_parallel,
          min_slice_bytes_for_replica_parallel,
          max_replicas_for_replica_parallel,
      )
      for arr in arrays
  ]
  # D2H copy is performed automatically as part of dispatcher call, but
  # we must set properties correctly to pass later consistency checks.
  return [
      dataclasses.replace(
          rslices,
          is_on_host=True,
          replica_slices=[
              dataclasses.replace(
                  rslice,
                  unsliced_data=np.asarray(rslice.data()),
                  slice_args=None,
              )
              for rslice in rslices.replica_slices
          ],
      )
      for rslices in rslices_per_array
  ]

