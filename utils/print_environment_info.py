import os
import sys

def print_environment_info(return_string: bool = False) -> str | None:
  """Returns a string containing local environment & JAX installation information.

  This is useful information to include when asking a question or filing a bug.

  Args: return_string (bool) : if True, return the string rather than printing
  to stdout.
  """
  from jax import version

  # TODO(jakevdp): should we include other info, e.g. jax.config.values?
  python_version = sys.version.replace('\n', ' ')
  info = textwrap.dedent(f"""\
  jax:    {version.__version__}
  jaxlib: {lib.version_str}
  numpy:  {np.__version__}
  python: {python_version}
  device info: {xb.devices()[0].device_kind}-{xb.device_count()}, {xb.local_device_count()} local devices"
  process_count: {xb.process_count()}
  platform: {platform.uname()}""")
  for key, value in os.environ.items():
    if key.startswith(("JAX_", "XLA_")):
      info += f"\n{key}={value}"
  nvidia_smi = try_nvidia_smi()
  if nvidia_smi:
    info += '\n\n$ nvidia-smi\n' + nvidia_smi
  if return_string:
    return info
  else:
    return print(info)

