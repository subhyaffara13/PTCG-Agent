
def _reflect_index_fixer(index: Array, size: int) -> Array:
    return jnp.floor_divide(_mirror_index_fixer(2*index+1, 2*size+1) - 1, 2)

