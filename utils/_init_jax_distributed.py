import logging
import os

def _init_jax_distributed():
  """Initializes JAX distributed system if not managed by XManager."""

  try:
    if _PATHWAYS_AVAILABLE and pathwaysutils.is_pathways_backend_used():
      pathwaysutils.initialize()
      logging.info('Pathways initialized.')
    else:
      jax_platforms = os.environ.get('JAX_PLATFORMS')
      jax_coordinator_address = os.environ.get('JAX_COORDINATOR_ADDRESS')
      jax_process_id = os.environ.get('JAX_PROCESS_ID')
      jax_num_processes = os.environ.get('JAX_NUM_PROCESSES')
      jax_coordinator_port = os.environ.get('JAX_COORDINATOR_PORT')
      logging.info('JAX_PLATFORMS: %s', jax_platforms)
      logging.info(
          'JAX_COORDINATOR_ADDRESS: %s',
          jax_coordinator_address,
      )
      logging.info('JAX_PROCESS_ID: %s', jax_process_id)
      logging.info('JAX_NUM_PROCESSES: %s', jax_num_processes)
      logging.info('JAX_COORDINATOR_PORT: %s', jax_coordinator_port)
      if jax_num_processes is not None:
        jax_num_processes = int(jax_num_processes)
      if jax_process_id is not None:
        jax_process_id = int(jax_process_id)
      jax.distributed.initialize(
          coordinator_address=jax_coordinator_address,
          num_processes=jax_num_processes,
          process_id=jax_process_id,
          initialization_timeout=600,
      )
      logging.info('JAX distributed system initialized.')
      logging.info('Default JAX backend: %s', jax.default_backend())
      logging.info('Available devices: %s', jax.devices())
  except Exception as e:  # pylint: disable=broad-exception-caught
    logging.warning(
        'Failed to initialize JAX distributed system: %s. '
        'This is expected if running in a single-process environment. '
        'Continuing as single-process.',
        e,
        exc_info=True,
    )

  logging.info('JAX process index: %d', jax.process_index())
  logging.info('JAX process count: %d', jax.process_count())
  logging.info('JAX device count: %d', jax.device_count())
  logging.info('JAX local device count: %d', jax.local_device_count())

