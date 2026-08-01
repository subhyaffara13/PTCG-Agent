
def _sync_deserialize_arrays(
    infos: Sequence[types.ParamInfo],
    args: Sequence[types.RestoreArgs],
    shardings: Sequence[jax.sharding.Sharding],
    metadata_key: str | None,
    array_metadata_store: array_metadata_store_lib.Store | None,
) -> Sequence[jax.Array]:
  """Deserializes arrays and applies array_metadata if available."""


  return asyncio_utils.run_sync(
      _deserialize_arrays(
          infos,
          args,
          shardings,
          metadata_key,
          array_metadata_store,
      )
  )

