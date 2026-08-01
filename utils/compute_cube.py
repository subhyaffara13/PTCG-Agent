
def compute_cube(side):
  return jnp.sum(jnp.ones((side, side)) * side)

