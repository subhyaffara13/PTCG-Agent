from typing import Any

def _replicated_abstract_state(metadata: Any) -> Any:
  """Builds an abstract state with every leaf replicated across local devices.

  Used when no `sharding_config_path` is supplied — convenient for inner-loop
  smoke against tiny fixtures where no real sharding decision needs to be made.
  Leaf shapes and dtypes come from the checkpoint metadata.

  Args:
    metadata: The checkpoint metadata pytree (shapes + dtypes per leaf).

  Returns:
    An abstract state pytree with every leaf replicated across local devices.
  """
  mesh = jax.sharding.Mesh(jax.devices(), ("data",))
  replicated = jax.sharding.NamedSharding(mesh, jax.sharding.PartitionSpec())
  return jax.tree.map(
      lambda x: jax.ShapeDtypeStruct(
          shape=x.shape, dtype=x.dtype, sharding=replicated
      ),
      metadata,
  )

