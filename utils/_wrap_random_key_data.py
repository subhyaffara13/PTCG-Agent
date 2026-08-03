import logging
from typing import Any, Dict

def _wrap_random_key_data(
    array_metadatas: Any,
    infos: Sequence[types.ParamInfo],
    deserialized_arrays: list[jax.Array],
) -> Sequence[jax.Array]:
  """Parse array_metadatas and wrap deserialized_arrays as random keys."""

  logging.vlog(1, 'array_metadatas = %s', array_metadatas)
  if not isinstance(array_metadatas, Dict):
    raise ValueError(
        'Expecting array_metadatas to be a "Dict" but got'
        f' {type(array_metadatas)}.'
    )

  # use the first available array_metadata
  array_metadatas_cache = {
      array_metadata.param_name: array_metadata
      for array_metadata in next(iter(array_metadatas.values()))
  }

  for i, (info, v) in enumerate(zip(infos, deserialized_arrays)):
    if meta := array_metadatas_cache.get(info.name):
      assert isinstance(
          meta, array_metadata_lib.SerializedArrayMetadata
      ), f'Expecting SerializedArrayMetadata but got {type(meta)}.'
      if meta.ext_metadata is None or not isinstance(meta.ext_metadata, dict):
        continue

      if impl := meta.ext_metadata.get(array_metadata_lib.RANDOM_KEY_IMPL):  # pytype: disable=attribute-error
        deserialized_arrays[i] = jax.random.wrap_key_data(v, impl=impl)
        logging.vlog(
            1,
            '%s: recreated as a random key: %s',
            info.name,
            deserialized_arrays[i],
        )

  return deserialized_arrays

