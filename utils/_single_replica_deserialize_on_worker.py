
def _single_replica_deserialize_on_worker(
    _,
    infos: Sequence[types.ParamInfo],
    args: Sequence[SingleReplicaArrayRestoreArgs],
    single_replica_shardings: Sequence[jax.sharding.Sharding],
    metadata_key: str | None,
):
  """Deserializes a single replica on a worker."""
  return asyncio_utils.run_sync(
      _deserialize_arrays(
          infos,
          args,
          single_replica_shardings,
          metadata_key,
          None,
      )
  )

