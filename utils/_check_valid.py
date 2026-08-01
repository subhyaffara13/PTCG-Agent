
def _check_valid(c_type: str):
  if (c_type not in {'device_host', 'device', 'tpu_sparsecore'}
      and not c_type.startswith("gpu_stream:")):
    raise ValueError(
        f'Invalid compute type {c_type}. Current supported values '
        'are `device_host`, `device`, `tpu_sparsecore`, and `gpu_stream:#`.')

