import json
from typing import Any

def get_write_request(
    location_path: str,
    name: str,
    jax_array: jax.Array,
    timeout: datetime.timedelta,
    return_dict: bool = False,
) -> str | Mapping[str, Any]:
  """Returns a string representation of the plugin program which writes the given jax_array to the given location."""
  sharding = jax_array.sharding
  assert isinstance(sharding, jax.sharding.Sharding), sharding

  timeout_seconds, timeout_fractional_seconds = divmod(
      timeout.total_seconds(), 1
  )
  timeout_nanoseconds = timeout_fractional_seconds * 1e9
  d = {
      "persistenceWriteRequest": {
          "b64_location": string_to_base64(location_path),
          "b64_name": string_to_base64(name),
          "b64_hlo_sharding_string": get_hlo_sharding_string(
              jax_array.sharding, len(jax_array.shape)
          ),
          "shape": jax_array.shape,
          "devices": {
              "device_ids": [
                  # pylint:disable=protected-access
                  device.id
                  for device in sharding._device_assignment
                  # pylint:enable=protected-access
              ],
          },
          "timeout": {
              "seconds": int(timeout_seconds),
              "nanos": int(timeout_nanoseconds),
          },
      }
  }

  if return_dict:
    return d
  return json.dumps(d)

