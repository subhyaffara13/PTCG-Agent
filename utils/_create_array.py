import logging
from typing import Any

def _create_array(f, args, state, npdict=None):
   #array = numpy.core.multiarray._reconstruct(*args)
    array = f(*args)
    array.__setstate__(state)
    if npdict is not None: # we also have saved state in __dict__
        array.__dict__.update(npdict)
    return array


def _create_array(
    spec: dict[str, Any], mesh: jax.sharding.Mesh | None
) -> jax.typing.ArrayLike:
  """Creates a jax.Array based on the spec.

  Args:
    spec: A dictionary defining the array properties. Example: {'dtype':
      'float32', 'shape': [32], 'sharding': [None]}
    mesh: The mesh to use for sharding. Required if 'sharding' is in spec.

  Returns:
    A jax array.
  """
  dtype = getattr(jnp, spec['dtype'])
  shape = tuple(spec['shape'])
  sharding_spec = spec.get('sharding')

  if sharding_spec is not None and mesh is None:
    raise ValueError('Mesh is required when sharding spec is provided.')

  if mesh is None:
    logging.info(
        'No mesh and sharding spec provided, create an array with no sharding.'
    )
    return jnp.asarray(
        np.random.normal(size=shape, scale=np.prod(shape)), dtype=dtype
    )
  else:
    if sharding_spec is None:
      logging.info(
          'No sharding spec provided, creating a fully replicated array.'
      )
      pspec = jax.sharding.PartitionSpec()
    else:
      pspec = jax.sharding.PartitionSpec(*sharding_spec)
    sharding = jax.sharding.NamedSharding(mesh, pspec)
    logging.info(
        'Creating sharded array with shape=%s, dtype=%s, sharding=%s',
        shape,
        dtype,
        sharding,
    )
    np_array = np.random.normal(size=shape, scale=np.prod(shape)).astype(dtype)
    return jax.make_array_from_callback(
        shape, sharding, lambda index: np_array[index]
    )

