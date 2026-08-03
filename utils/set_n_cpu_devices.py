import os
import re
from typing import Optional

def set_n_cpu_devices(n: Optional[int] = None) -> None:
  """Forces XLA to use `n` CPU threads as host devices.

  This allows `jax.pmap` to be tested on a single-CPU platform.
  This utility only takes effect before XLA backends are initialized, i.e.
  before any JAX operation is executed (including `jax.devices()` etc.).
  See https://github.com/google/jax/issues/1408.

  Args:
    n: A required number of CPU devices (``FLAGS.chex_n_cpu_devices`` is used by
      default).

  Raises:
    RuntimeError: If XLA backends were already initialized.
  """
  n = n or FLAGS['chex_n_cpu_devices'].value

  n_devices = get_n_cpu_devices_from_xla_flags()
  cpu_backend = (jax._src.xla_bridge._backends or {}).get('cpu', None)  # pylint: disable=protected-access
  if cpu_backend is not None and n_devices != n:
    raise RuntimeError(
        f'Attempted to set {n} devices, but {n_devices} CPUs already available:'
        ' ensure that `set_n_cpu_devices` is executed before any JAX operation.'
    )

  xla_flags = os.getenv('XLA_FLAGS', '')
  xla_flags = re.sub(_xla_device_count_flag_regexp, '', xla_flags)
  os.environ['XLA_FLAGS'] = ' '.join(
      [f'--xla_force_host_platform_device_count={n}'] + xla_flags.split())

