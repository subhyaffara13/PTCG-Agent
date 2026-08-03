import os
from typing import Any

def verify_tensorstore_spec(spec: dict[str, Any], arr: jax.Array | None,
                            path: str | os.PathLike[str], ocdbt: bool,
                            check_metadata: bool = True) -> None:
  """Verify the minimum requirements for a tensorstore spec."""
  if ocdbt:
    if spec.get("kvstore", {}).get("driver", "") != "ocdbt":
      raise ValueError(f"Expected ocdbt driver, got {spec=}")
  if check_metadata:
    if arr is None:
      raise ValueError("Array is required for metadata verification.")
    metadata = spec['metadata']
    if spec.get("driver", "") == "zarr3":
      if metadata['data_type'] != jnp.dtype(arr.dtype).name:
        raise ValueError(f"Provided dtype ({metadata['data_type']=}) doesn't"
                         f" match ({arr.dtype=})")
    if 'shape' in metadata:
      if metadata['shape'] != arr.shape:
        raise ValueError(f"Provided shape ({metadata['shape']=}) doesn't match"
                         f" ({arr.shape=})")
    if isinstance(arr, jax.Array):
      local_shape = arr.sharding.shard_shape(arr.shape)
    else:  # np.ndarray
      local_shape = arr.shape
    if spec.get("driver", "") == "zarr3":
      chunk_shape = metadata['chunk_grid']['configuration']['chunk_shape']
      if not _divides(local_shape, chunk_shape):
        raise ValueError(f"Provided chunk shape {chunk_shape} does not divide"
                         f" the local shape of the array {local_shape}")
  # check path is still the same one we expect
  if ocdbt:
    found_path = spec["kvstore"]['base']['path']
  else:
    found_path = spec["kvstore"]['path']
  if str(found_path) != str(path):
    raise ValueError(f"Provided {path=} does not match the spec path:"
                     f" {spec['kvstore']}")

