import os
from typing import Any

def generate_pjrt_gpu_plugin_options() -> _NameValueMapping:
  """Generates the PjRt GPU plugin options.

  Returns:
    A dictionary of plugin options.
  """

  options: dict[str, Any] = {}
  options['platform_name'] = 'cuda'
  allocator = os.getenv('XLA_PYTHON_CLIENT_ALLOCATOR', 'default').lower()
  memory_fraction = os.getenv('XLA_CLIENT_MEM_FRACTION', '')
  deprecated_memory_fraction = os.getenv('XLA_PYTHON_CLIENT_MEM_FRACTION', '')
  if deprecated_memory_fraction:
    if memory_fraction:
      raise ValueError(
          'XLA_CLIENT_MEM_FRACTION is specified together '
          'with XLA_PYTHON_CLIENT_MEM_FRACTION. '
          'Remove the latter one, it is deprecated.'
      )
    else:
      memory_fraction = deprecated_memory_fraction
  preallocate = os.getenv('XLA_PYTHON_CLIENT_PREALLOCATE', '')
  collective_memory_size = os.getenv(
      'XLA_PYTHON_CLIENT_COLLECTIVE_MEM_SIZE_MB', ''
  )
  if allocator not in ('default', 'platform', 'bfc', 'cuda_async', 'vmm'):
    raise ValueError(
        'XLA_PYTHON_CLIENT_ALLOCATOR env var must be "default", "platform", '
        '"bfc", "cuda_async", or "vmm", got "%s"' % allocator
    )
  options['allocator'] = allocator
  if memory_fraction:
    options['memory_fraction'] = float(memory_fraction)
  if preallocate:
    options['preallocate'] = preallocate not in ('false', 'False', '0')
  if collective_memory_size:
    options['collective_memory_size'] = int(collective_memory_size) * (1 << 20)
  abort = os.getenv('XLA_PYTHON_CLIENT_ABORT_COLLECTIVES_ON_FAILURE', '0')
  options['abort_collectives_on_failure'] = bool(int(abort))
  use_trft_gpu_client = os.getenv('XLA_PYTHON_CLIENT_USE_TFRT_GPU_CLIENT', '0')
  options['use_tfrt_gpu_client'] = bool(int(use_trft_gpu_client))
  return options

