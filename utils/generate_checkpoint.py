import logging
from typing import Any

def generate_checkpoint(
    config: configs.CheckpointConfig, mesh: jax.sharding.Mesh | None = None
) -> Any:
  """Generates a PyTree of test checkpoint data based on a provided specification.

  Args:
      config: A CheckpointConfig object containing the data specification.
      mesh: The mesh to use for sharding the generated data. If None, the data
        will not be sharded.

  Returns:
      A dictionary (PyTree) containing the generated data.

  Raises:
      ValueError: If the spec string is not supported.
  """
  if config.spec is None:
    raise ValueError(
        'CheckpointConfig must have a `spec` if `path` is not provided.'
    )
  pytree = {}
  if config.random_seed is not None:
    np.random.seed(config.random_seed)

  for name, spec in config.spec.items():
    if isinstance(spec, str):
      if spec == 'int':
        pytree[name] = 0
      elif spec == 'str':
        pytree[name] = 'default_string'
      else:
        raise ValueError(f'Unsupported spec string: {spec}')
    elif isinstance(spec, dict):
      pytree[name] = _create_array(spec, mesh)
    else:
      raise ValueError(f'Unsupported spec type: {type(spec)}')
  logging.info('Generated data with keys: %s', list(pytree.keys()))
  return pytree

