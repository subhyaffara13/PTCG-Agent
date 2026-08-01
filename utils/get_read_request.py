
def get_read_request(
    location_path: str,
    name: str,
    dtype: np.dtype,
    shape: Sequence[int],
    sharding: jax.sharding.Sharding,
    devices: Sequence[jax.Device],
    timeout: datetime.timedelta,
    return_dict: bool = False,
) -> str | Mapping[str, Any]:
  """Returns a string representation of the plugin program which reads the given array from the given location into the provided sharding."""
  if not isinstance(devices, np.ndarray):
    devices = np.array(devices)

  timeout_seconds, timeout_fractional_seconds = divmod(
      timeout.total_seconds(), 1
  )
  timeout_nanoseconds = timeout_fractional_seconds * 1e9
  d = {
      "persistenceReadRequest": {
          "b64_location": string_to_base64(location_path),
          "shape": get_shape_info(dtype, shape),
          "b64_name": string_to_base64(name),
          "b64_hlo_sharding_string": get_hlo_sharding_string(
              sharding, len(shape)
          ),
          "devices": {
              "device_ids": [device.id for device in devices.flatten()]
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

