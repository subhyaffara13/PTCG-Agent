from typing import Any

def _serialize(obj: Any) -> bytes:
  """Serializes callables and input/output spec objects.

  DO NOT USE THIS FUNCTION EXCEPT FOR THE INTERNAL IMPLEMENTATION OF
  colocated_python.

  This module contains utility functions used internally for implementiong
  `colocated_python` when it ships callables and input/output specs through
  IFRT. The pickled data is produced and consumed in an ephermeral fashion
  without any persistence, and it does not expect any version compatibility
  (which cloudpickle does not guarantee). Furthermore, serialization and
  deserialization is expected to be done on machine(s) that are controlled by a
  single tenant, which allows unpickling done during deserialization to be
  trusted.

  Raises:
    ModuleNotFoundError: If cloudpickle is not available.
  """
  if cloudpickle is None:
    raise ModuleNotFoundError('No module named "cloudpickle"')

  class _CustomPickler(cloudpickle.Pickler):
    dispatch_table = collections.ChainMap(
        {jax.sharding.Mesh: _reduce_mesh},
        {jax.sharding.NamedSharding: _reduce_named_sharding},  # pyrefly: ignore[bad-argument-type]
        {DeviceList: _reduce_device_list},  # pyrefly: ignore[bad-argument-type]
        {jax.sharding.SingleDeviceSharding: _reduce_single_device_sharding},  # pyrefly: ignore[bad-argument-type]
        cloudpickle.CloudPickler.dispatch_table,  # pyrefly: ignore[bad-argument-type]
    )
    dispatch = dispatch_table

  assert _common_obj_state.common_obj_index is None, (
      "_serialize() expects no recursive calls")
  _common_obj_state.common_obj_index = {}
  try:
    with io.BytesIO() as file:
      _CustomPickler(file).dump(obj)
      return file.getvalue()
  finally:
    _common_obj_state.common_obj_index = None

