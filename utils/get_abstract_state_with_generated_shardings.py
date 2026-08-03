from typing import Any

def get_abstract_state_with_generated_shardings(pytree_metadata: Any) -> Any:
  abstract_state = jax.tree.map(
      abstract_arrays.to_shape_dtype_struct, pytree_metadata
  )
  shardings = sharding_utils.construct_maximal_shardings(abstract_state)
  return jax.tree.map(
      lambda sds, sharding: jax.ShapeDtypeStruct(
          sds.shape, sds.dtype, sharding=sharding
      ),
      abstract_state,
      shardings,
  )

